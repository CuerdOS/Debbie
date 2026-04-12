#!/usr/bin/env python3
"""
Debbie – Instalador de paquetes .deb
Puerto a PySide6 / Qt 6 nativo.
El diálogo «Acerca de» sigue el mismo diseño que Éclair.
"""
import os
import sys
import subprocess
import hashlib
import locale
import json
import threading
import time
from pathlib import Path

# ── Traducciones ──────────────────────────────────────────────────────────────
try:
    import translations as _translations
    from translations import _, set_language
except ImportError:
    class _translations:
        current_language = "en"
    def _(text): return text
    def set_language(lang):
        _translations.current_language = lang

# ── Qt 6 ──────────────────────────────────────────────────────────────────────
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QToolBar,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QFrame, QGroupBox,
    QProgressBar, QStatusBar, QFileDialog,
    QMessageBox, QDialog, QDialogButtonBox, QComboBox,
    QSizePolicy,
)
from PySide6.QtCore import (
    Qt, QSize, QMimeData, QUrl, Signal, QObject, QTimer,
)
from PySide6.QtGui import (
    QIcon, QPixmap, QAction, QDragEnterEvent, QDropEvent,
    QDragLeaveEvent,
)

# ── Rutas de configuración ────────────────────────────────────────────────────
CONFIG_DIR  = Path.home() / ".config" / "debbie"
CONFIG_FILE = CONFIG_DIR  / "config.json"


# ═════════════════════════════════════════════════════════════════════════════
# Hoja de estilos Qt (QSS) — misma filosofía que Éclair
# ═════════════════════════════════════════════════════════════════════════════
STYLESHEET = """
QMainWindow, QWidget#centralWidget {
    background-color: palette(window);
}

/* ── Barra de herramientas ── */
QToolBar {
    background-color: palette(window);
    border-bottom: 1px solid palette(mid);
    spacing: 4px;
    padding: 2px 4px;
}
QToolBar QToolButton {
    padding: 4px 8px;
    border-radius: 5px;
    background: transparent;
}
QToolBar QToolButton:hover {
    background-color: rgba(128,128,128,30);
}
QToolBar QToolButton:pressed {
    background-color: rgba(128,128,128,60);
}

/* ── Botón acción principal ── */
QPushButton#actionButton {
    border-radius: 6px;
    padding: 5px 20px;
    min-height: 30px;
    background-color: palette(highlight);
    color: palette(highlighted-text);
    font-weight: bold;
    border: none;
}
QPushButton#actionButton:hover {
    border: 1px solid palette(highlighted-text);
}
QPushButton#actionButton:pressed {
    background-color: palette(dark);
    color: palette(window-text);
}
QPushButton#actionButton:disabled {
    background-color: palette(mid);
    color: palette(dark);
}

/* ── Botón destructivo (Eliminar) ── */
QPushButton#removeButton {
    border-radius: 6px;
    padding: 5px 16px;
    min-height: 30px;
    background-color: #c01c28;
    color: #ffffff;
    font-weight: bold;
    border: none;
}
QPushButton#removeButton:hover {
    background-color: #e01b24;
}
QPushButton#removeButton:pressed {
    background-color: #a01020;
}
QPushButton#removeButton:disabled {
    background-color: palette(mid);
    color: palette(dark);
}

/* ── Botón cancelar ── */
QPushButton#cancelButton {
    border-radius: 6px;
    padding: 5px 16px;
    min-height: 30px;
}

/* ── GroupBox (equivale a Gtk.Frame) ── */
QGroupBox {
    font-weight: bold;
    border: 1px solid palette(mid);
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 6px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: palette(window-text);
}

/* ── ScrollArea ── */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}

/* ── Barra de estado ── */
QStatusBar {
    border-top: 1px solid palette(mid);
    padding: 1px 4px;
}

/* ── ProgressBar ── */
QProgressBar {
    border: 1px solid palette(mid);
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: palette(highlight);
    border-radius: 3px;
}

/* ── Drop overlay ── */
QWidget#dropOverlay {
    background-color: rgba(53, 132, 228, 0.25);
    border: 3px dashed rgba(53, 132, 228, 0.8);
    border-radius: 10px;
}
"""


# ═════════════════════════════════════════════════════════════════════════════
# Helpers de estado
# ═════════════════════════════════════════════════════════════════════════════

class AuthCache:
    """Singleton para cachear la autenticación pkexec durante 5 min."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._auth_time = 0.0
            cls._instance._auth_duration = 300.0
        return cls._instance

    def is_authenticated(self):
        return time.time() - self._auth_time < self._auth_duration

    def set_authenticated(self):
        self._auth_time = time.time()


class PackageHistory:
    """Historial de las últimas 50 operaciones."""
    def __init__(self):
        self.history_file = CONFIG_DIR / "history.json"
        self.history = self._load_history()

    def _load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def add_package(self, package_name, action, file_path):
        entry = {
            'package':   package_name,
            'action':    action,
            'file':      os.path.basename(file_path) if file_path else package_name,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        self.history.insert(0, entry)
        self.history = self.history[:50]
        self._save_history()

    def _save_history(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_recent_packages(self, limit=10):
        return self.history[:limit]


# ═════════════════════════════════════════════════════════════════════════════
# Bridge de señales para comunicación hilo → UI
# ═════════════════════════════════════════════════════════════════════════════

class WorkerSignals(QObject):
    append_output  = Signal(str)
    process_done   = Signal(bool, str, str, str)   # success, msg, pkg, action
    finish_process = Signal()


# ═════════════════════════════════════════════════════════════════════════════
# Ventana principal
# ═════════════════════════════════════════════════════════════════════════════

class DebInstaller(QMainWindow):
    def __init__(self, file_path=None):
        self._init_language()

        super().__init__()
        self.setWindowTitle(_("title"))
        self.resize(700, 520)
        self._center_window()

        # Icono
        self._setup_window_icon()

        # Estado
        self.package_cache         = {}
        self.current_file_path     = None
        self.current_process       = None
        self.is_running_process    = False
        self.process_cancelled     = False
        self.auth_cache            = AuthCache()
        self.package_history       = PackageHistory()
        self.original_argv         = sys.argv.copy()
        self.signals               = WorkerSignals()

        # Conectar señales de hilo → UI
        self.signals.append_output.connect(self._append_to_output)
        self.signals.process_done.connect(self._on_process_done)
        self.signals.finish_process.connect(self._finish_process)

        # Timer para pulsar la barra de progreso
        self._progress_timer = QTimer(self)
        self._progress_timer.timeout.connect(self._pulse_progress)
        self._progress_value = 0

        self._setup_ui()
        self.setAcceptDrops(True)

        # Cargar archivo si se proporcionó
        if file_path and os.path.exists(file_path) and file_path.endswith('.deb'):
            self._load_package(file_path)

    # ── Inicialización de idioma ─────────────────────────────────────────────

    def _init_language(self):
        lang = None
        language_auto = True

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    language_auto = config.get('language_auto', True)
                    if not language_auto:
                        lang = config.get('language')
            except Exception:
                pass

        if language_auto or not lang:
            lang = self._get_system_language()
            if not CONFIG_FILE.exists():
                self._save_config(lang, language_auto=True)

        set_language(lang)

    def _get_system_language(self):
        supported = {"es", "en", "pt", "it", "de", "ja", "ko", "ca"}

        for env_var in ('LANG', 'LC_ALL', 'LC_MESSAGES'):
            val = os.environ.get(env_var, '')
            code = val.split('_')[0].split('.')[0].lower()
            if code and code != 'c' and code in supported:
                return code

        try:
            loc = locale.getlocale()[0] or ''
            code = loc.split('_')[0].lower()
            if code in supported:
                return code
        except Exception:
            pass

        return 'es'

    def _get_language_auto(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f).get('language_auto', True)
            except Exception:
                pass
        return True

    def get_current_language(self):
        try:
            return _translations.current_language
        except Exception:
            return 'en'

    def _save_config(self, language, language_auto=False):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'language': language, 'language_auto': language_auto},
                          f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    # ── Icono de ventana ─────────────────────────────────────────────────────

    def _setup_window_icon(self):
        icon_paths = [
            "debbie.svg",
            "icons/debbie.svg",
            os.path.join(os.path.dirname(__file__), "debbie.svg"),
            os.path.join(os.path.dirname(__file__), "icons", "debbie.svg"),
            "/usr/share/debbie/debbie.svg",
            "/usr/share/icons/hicolor/scalable/apps/debbie.svg",
            "/usr/share/pixmaps/debbie.svg",
        ]
        for path in icon_paths:
            if os.path.exists(path):
                self.setWindowIcon(QIcon(path))
                return
        self.setWindowIcon(QIcon.fromTheme("package-x-generic"))

    def _center_window(self):
        screen = QApplication.primaryScreen()
        if screen:
            geom  = screen.availableGeometry()
            fg    = self.frameGeometry()
            fg.moveCenter(geom.center())
            self.move(fg.topLeft())

    # ── Construcción de la UI ────────────────────────────────────────────────

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Toolbar
        self._create_toolbar()

        # Área de contenido
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 12, 16, 8)
        content_layout.setSpacing(8)

        # Overlay de drag & drop (invisible por defecto)
        self.drop_overlay = QWidget(central)
        self.drop_overlay.setObjectName("dropOverlay")
        self.drop_overlay.hide()
        self._build_drop_overlay_content()

        # Info de archivo
        self.file_label           = QLabel(_("no_file"))
        self.version_status_label = QLabel("")
        self.package_details      = QLabel("")
        self.package_details.setTextFormat(Qt.TextFormat.RichText)

        for lbl in (self.file_label, self.version_status_label, self.package_details):
            lbl.setWordWrap(True)
            content_layout.addWidget(lbl)

        # GroupBox: Información del paquete
        self.info_group  = QGroupBox(_("package_information"))
        info_layout      = QVBoxLayout(self.info_group)
        self.info_view   = QTextEdit()
        self.info_view.setReadOnly(True)
        self.info_view.setMinimumHeight(120)
        self.info_view.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Expanding)
        info_layout.addWidget(self.info_view)
        content_layout.addWidget(self.info_group, stretch=2)

        # GroupBox: Salida de instalación
        self.output_group  = QGroupBox(_("installation_output"))
        output_layout      = QVBoxLayout(self.output_group)
        self.output_view   = QTextEdit()
        self.output_view.setReadOnly(True)
        self.output_view.setMinimumHeight(150)
        self.output_view.setFontFamily("monospace")
        self.output_view.setSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding)
        output_layout.addWidget(self.output_view)
        self.output_group.hide()
        content_layout.addWidget(self.output_group, stretch=3)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)   # modo indeterminado
        self.progress_bar.hide()
        content_layout.addWidget(self.progress_bar)

        # Botones de acción
        btn_widget = self._create_button_row()
        content_layout.addWidget(btn_widget)

        root.addWidget(content_widget, stretch=1)

        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(_("ready"))

    def _build_drop_overlay_content(self):
        layout = QVBoxLayout(self.drop_overlay)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel()
        icon = QIcon.fromTheme("package-x-generic")
        if not icon.isNull():
            icon_lbl.setPixmap(icon.pixmap(QSize(96, 96)))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_lbl)

        text_lbl = QLabel(
            f"<span style='font-size:18pt; font-weight:bold'>{_('drop_deb_here')}</span><br>"
            f"<span style='font-size:12pt; opacity:0.7'>{_('or_click_to_open')}</span>"
        )
        text_lbl.setTextFormat(Qt.TextFormat.RichText)
        text_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_lbl)

    def _create_toolbar(self):
        tb = QToolBar()
        tb.setIconSize(QSize(22, 22))
        tb.setMovable(False)
        tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.addToolBar(tb)

        open_act = QAction(QIcon.fromTheme("document-open"), _("Open"), self)
        open_act.setToolTip(_("open_deb"))
        open_act.triggered.connect(lambda: self.on_open_clicked())
        tb.addAction(open_act)

        extract_act = QAction(QIcon.fromTheme("package"), _("Extract"), self)
        extract_act.setToolTip(_("extract_package"))
        extract_act.triggered.connect(lambda: self.on_extract_clicked())
        tb.addAction(extract_act)

        tb.addSeparator()

        # Espaciador flexible
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Preferred)
        tb.addWidget(spacer)

        lang_act = QAction(QIcon.fromTheme("preferences-desktop-locale"),
                           _("Language"), self)
        lang_act.setToolTip(_("change_language"))
        lang_act.triggered.connect(lambda: self.show_language_selector())
        tb.addAction(lang_act)

        about_act = QAction(QIcon.fromTheme("help-about"), _("About"), self)
        about_act.setToolTip(_("about"))
        about_act.triggered.connect(lambda: self.show_about_dialog())
        tb.addAction(about_act)

    def _create_button_row(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Botón Eliminar
        self.remove_button = QPushButton(_("remove"))
        self.remove_button.setObjectName("removeButton")
        self.remove_button.setIcon(QIcon.fromTheme("user-trash"))
        self.remove_button.setEnabled(False)
        self.remove_button.hide()
        self.remove_button.clicked.connect(self.on_remove_clicked)
        layout.addWidget(self.remove_button)

        layout.addStretch()

        # Botón Cancelar
        self.cancel_button = QPushButton(_("cancel"))
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.setIcon(QIcon.fromTheme("process-stop"))
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        layout.addWidget(self.cancel_button)

        # Botón Instalar / Actualizar / …
        self.action_button = QPushButton(_("install"))
        self.action_button.setObjectName("actionButton")
        self.action_button.setIcon(QIcon.fromTheme("system-software-install"))
        self.action_button.setEnabled(False)
        self.action_button.clicked.connect(self.on_install_clicked)
        layout.addWidget(self.action_button)

        return widget

    # ── Drag & Drop ──────────────────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'drop_overlay'):
            cw = self.centralWidget()
            if cw:
                self.drop_overlay.setGeometry(cw.geometry())

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(u.toLocalFile().endswith('.deb') for u in urls):
                event.acceptProposedAction()
                self._show_drop_overlay(True)
                return
        event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self._show_drop_overlay(False)

    def dropEvent(self, event: QDropEvent):
        self._show_drop_overlay(False)
        urls = event.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            if path.endswith('.deb') and os.path.exists(path):
                self._load_package(path)
                event.acceptProposedAction()
                return
        QMessageBox.information(self, _("error"), _("not_deb_file"))

    def _show_drop_overlay(self, visible: bool):
        if not hasattr(self, 'drop_overlay'):
            return
        if visible:
            cw = self.centralWidget()
            if cw:
                self.drop_overlay.setGeometry(cw.geometry())
            self.drop_overlay.raise_()
            self.drop_overlay.show()
        else:
            self.drop_overlay.hide()

    # ── Acciones de toolbar ──────────────────────────────────────────────────

    def on_open_clicked(self):
        path, _filter = QFileDialog.getOpenFileName(
            self, _("select_deb_file"), "",
            f"{_('deb_packages')} (*.deb)"
        )
        if path:
            self._load_package(path)

    def on_extract_clicked(self):
        if not self.current_file_path:
            QMessageBox.information(self, _("error"), _("no_package_loaded"))
            return
        folder = QFileDialog.getExistingDirectory(
            self, _("select_extraction_folder")
        )
        if folder:
            self._extract_package(self.current_file_path, folder)

    # ── Carga de paquete ─────────────────────────────────────────────────────

    def _load_package(self, file_path):
        if not os.path.exists(file_path):
            QMessageBox.warning(self, _("error"), _("file_not_found"))
            return

        self.current_file_path = file_path
        self.file_label.setText(f"{_('file')}: {os.path.basename(file_path)}")

        file_hash = self._calculate_file_hash(file_path)
        if file_hash in self.package_cache:
            package_info = self.package_cache[file_hash]
        else:
            package_info = self._get_package_info(file_path)
            if package_info:
                self.package_cache[file_hash] = package_info

        if package_info:
            self._display_package_info(package_info)
            self._update_action_button_with_version_check(
                package_info.get('Package', 'Unknown'), file_path
            )
        else:
            QMessageBox.warning(self, _("error"), _("failed_to_load_package_info"))

    def _calculate_file_hash(self, file_path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _get_package_info(self, file_path):
        try:
            result = subprocess.run(
                ['dpkg-deb', '-I', file_path],
                capture_output=True, text=True, check=True
            )
            info = {}
            for line in result.stdout.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            return info
        except subprocess.CalledProcessError as e:
            print(f"Error getting package info: {e}")
            return None

    def _display_package_info(self, info):
        package_name = info.get('Package', _('unknown'))
        deb_version  = info.get('Version',  _('unknown'))

        self.package_details.setText(
            f"<b>{_('package')}:</b> {package_name} &nbsp;|&nbsp; "
            f"<b>{_('version')}:</b> {deb_version}"
        )

        self.info_view.setPlainText(
            "\n".join(f"{k}: {v}" for k, v in info.items())
        )
        self.status_bar.showMessage(f"{_('loaded')}: {package_name}")

    def _update_action_button_with_version_check(self, package_name, deb_file):
        from packaging import version as pkg_version

        installed = self._get_installed_version(package_name)
        deb_ver   = self._get_deb_version(deb_file)

        if installed:
            self.remove_button.setEnabled(True)
            self.remove_button.show()
            try:
                if pkg_version.parse(deb_ver) > pkg_version.parse(installed):
                    status = f"📦 {_('upgrade_available')}: {installed} → {deb_ver}"
                    btn_lbl = _("upgrade")
                elif pkg_version.parse(deb_ver) < pkg_version.parse(installed):
                    status = f"⬇️ {_('downgrade_warning')}: {installed} → {deb_ver}"
                    btn_lbl = _("downgrade")
                else:
                    status = f"✅ {_('same_version_installed')}: {installed}"
                    btn_lbl = _("reinstall")
            except Exception:
                status  = f"✅ {_('installed_version')}: {installed} | {_('deb_version')}: {deb_ver}"
                btn_lbl = _("reinstall")

            self.version_status_label.setText(f"<b>{status}</b>")
            self.version_status_label.setTextFormat(Qt.TextFormat.RichText)
            self.action_button.setText(btn_lbl)
        else:
            self.remove_button.setEnabled(False)
            self.remove_button.hide()
            self.version_status_label.setText(f"<b>ℹ️ {_('not_installed')}</b>")
            self.version_status_label.setTextFormat(Qt.TextFormat.RichText)
            self.action_button.setText(_("install"))

        self.action_button.setEnabled(True)

    def _get_installed_version(self, package_name):
        try:
            result = subprocess.run(
                ['dpkg-query', '-W', '-f=${Version}', package_name],
                capture_output=True, text=True
            )
            return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None
        except Exception:
            return None

    def _get_deb_version(self, deb_file):
        try:
            result = subprocess.run(
                ['dpkg-deb', '-f', deb_file, 'Version'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"

    # ── Instalar / Eliminar ──────────────────────────────────────────────────

    def on_install_clicked(self):
        if not self.current_file_path:
            return
        if self.is_running_process:
            QMessageBox.information(self, _("error"), _("process_already_running"))
            return
        pkg = self._get_package_name_from_file(self.current_file_path)
        reply = QMessageBox.question(
            self, _("confirm_install"),
            f"{_('confirm_install')} {pkg}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._start_installation(self.current_file_path, pkg)

    def on_remove_clicked(self):
        if not self.current_file_path:
            return
        if self.is_running_process:
            QMessageBox.information(self, _("error"), _("process_already_running"))
            return
        pkg = self._get_package_name_from_file(self.current_file_path)
        reply = QMessageBox.question(
            self, _("confirm_remove"),
            f"{_('confirm_remove')} {pkg}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._start_removal(pkg)

    def on_cancel_clicked(self):
        if self.is_running_process and self.current_process:
            self.process_cancelled = True
            try:
                self.current_process.terminate()
                self._append_to_output(f"\n{_('process_cancelled')}")
            except Exception:
                pass

    def _get_package_name_from_file(self, deb_file):
        try:
            result = subprocess.run(
                ['dpkg-deb', '-f', deb_file, 'Package'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"

    # ── Proceso de instalación ───────────────────────────────────────────────

    def _start_installation(self, deb_file, package_name):
        self._begin_process(f"{_('installing')} {package_name}...")
        t = threading.Thread(
            target=self._install_package_thread,
            args=(deb_file, package_name), daemon=True
        )
        t.start()

    def _start_removal(self, package_name):
        self._begin_process(f"{_('removing')} {package_name}...")
        self.remove_button.setEnabled(False)
        t = threading.Thread(
            target=self._remove_package_thread,
            args=(package_name,), daemon=True
        )
        t.start()

    def _begin_process(self, status_msg):
        self.is_running_process = True
        self.action_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.show()
        self._progress_value = 0
        self._progress_timer.start(80)
        self.output_view.clear()
        self.output_group.show()
        self.status_bar.showMessage(status_msg)

    def _pulse_progress(self):
        if self.is_running_process:
            # Simulamos pulsado desplazando manualmente el valor
            self._progress_value = (self._progress_value + 5) % 100
        else:
            self._progress_timer.stop()

    def _install_package_thread(self, deb_file, package_name):
        try:
            self.auth_cache.set_authenticated()
            cmd = ['pkexec', 'apt-get', 'install', '-y',
                   '--reinstall', '--allow-downgrades', deb_file]
            self.current_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            if self.current_process.stdout:
                for line in self.current_process.stdout:
                    if self.process_cancelled:
                        break
                    self.signals.append_output.emit(line.rstrip())
            self.current_process.wait()
            if self.process_cancelled:
                self.signals.finish_process.emit()
                return
            if self.current_process.returncode == 0:
                self.signals.process_done.emit(
                    True, _("package_installed_successfully"),
                    package_name, "installed"
                )
            else:
                self.signals.process_done.emit(
                    False, _("installation_failed"), package_name, ""
                )
        except Exception as e:
            self.signals.process_done.emit(
                False, f"{_('unexpected_error')}\n{e}", package_name, ""
            )
        finally:
            self.signals.finish_process.emit()

    def _remove_package_thread(self, package_name):
        try:
            self.auth_cache.set_authenticated()
            cmd = ['pkexec', 'apt-get', 'remove', '-y', package_name]
            self.current_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            if self.current_process.stdout:
                for line in self.current_process.stdout:
                    if self.process_cancelled:
                        break
                    self.signals.append_output.emit(line.rstrip())
            self.current_process.wait()
            if self.process_cancelled:
                self.signals.finish_process.emit()
                return
            if self.current_process.returncode == 0:
                self.signals.process_done.emit(
                    True, _("package_removed_successfully"),
                    package_name, "removed"
                )
            else:
                self.signals.process_done.emit(
                    False, _("removal_failed"), package_name, ""
                )
        except Exception as e:
            self.signals.process_done.emit(
                False, f"{_('unexpected_error')}\n{e}", package_name, ""
            )
        finally:
            self.signals.finish_process.emit()

    # ── Slots de señales de hilo ─────────────────────────────────────────────

    def _append_to_output(self, message: str):
        self.output_view.append(message)
        sb = self.output_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _on_process_done(self, success: bool, message: str,
                         package_name: str, action_type: str):
        if success:
            self._append_to_output(f"\n✅ {message}")
            if action_type == "installed" and self.current_file_path:
                self.package_history.add_package(
                    package_name, action_type, self.current_file_path
                )
            elif action_type == "removed":
                self.package_history.add_package(package_name, action_type, None)
            self._send_notification("Debbie", f"{message}: {package_name}")
        else:
            self._append_to_output(f"\n❌ {message}")
            QMessageBox.warning(self, _("error"), message)
            self._send_notification("Debbie Error",
                                    f"{_('operation_failed')}: {package_name}")

        if self.current_file_path:
            self._update_action_button_with_version_check(
                package_name, self.current_file_path
            )

    def _finish_process(self):
        self._progress_timer.stop()
        self.is_running_process   = False
        self.current_process      = None
        self.process_cancelled    = False
        self.action_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.hide()
        self.status_bar.showMessage(_("ready"))
        self.raise_()
        self.activateWindow()

    def _send_notification(self, title, message):
        try:
            subprocess.Popen(["notify-send", "-i", "debbie", title, message])
        except Exception:
            pass

    # ── Extracción ───────────────────────────────────────────────────────────

    def _extract_package(self, deb_file, extract_path):
        try:
            pkg_name         = os.path.splitext(os.path.basename(deb_file))[0]
            full_extract     = os.path.join(extract_path, pkg_name)
            os.makedirs(full_extract, exist_ok=True)
            result = subprocess.run(
                f"dpkg-deb -x '{deb_file}' '{full_extract}'",
                shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                QMessageBox.information(
                    self, _("success"),
                    f"{_('package_extracted_to')} {full_extract}"
                )
                subprocess.Popen(["xdg-open", full_extract])
            else:
                QMessageBox.warning(
                    self, _("error"),
                    f"{_('extraction_failed')}\n{result.stderr}"
                )
        except Exception as e:
            QMessageBox.warning(self, _("error"), f"{_('extraction_failed')}\n{e}")

    # ── Selector de idioma ───────────────────────────────────────────────────

    def show_language_selector(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(_("select_language"))
        dlg.setModal(True)
        dlg.setMinimumWidth(260)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        layout.addWidget(QLabel(_("select_language") + ":"))

        combo = QComboBox()
        languages = [
            ("auto", "AUTO"),
            ("en",   "English"),
            ("es",   "Español"),
            ("ja",   "日本語"),
            ("pt",   "Português"),
            ("de",   "Deutsch"),
            ("ko",   "한국어"),
            ("it",   "Italiano"),
            ("ca",   "Català"),
        ]
        for code, name in languages:
            combo.addItem(name, code)

        if self._get_language_auto():
            idx = next((i for i, (c, _) in enumerate(languages) if c == "auto"), 0)
        else:
            current = self.get_current_language()
            idx = next((i for i, (c, _) in enumerate(languages) if c == current), 0)
        combo.setCurrentIndex(idx)
        layout.addWidget(combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            lang_code = combo.currentData()
            if lang_code:
                if lang_code == "auto":
                    detected = self._get_system_language()
                    self._save_config(detected, language_auto=True)
                else:
                    self._save_config(lang_code, language_auto=False)

                # Reiniciar la aplicación para aplicar el idioma
                reply = QMessageBox.question(
                    self, "Restart / Reiniciar",
                    "The application will restart to apply the new language.\n"
                    "La aplicación se reiniciará para aplicar el nuevo idioma.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    QApplication.instance().quit()
                    subprocess.Popen([sys.executable] + self.original_argv)

    # ── Diálogo Acerca de (diseño Éclair) ────────────────────────────────────

    def show_about_dialog(self):
        """Diálogo Acerca de con el mismo diseño que Éclair."""
        dlg = QDialog(self)
        dlg.setWindowTitle(f"{_('about')} Debbie")
        dlg.setModal(True)
        dlg.setMinimumWidth(340)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 16)
        layout.setSpacing(8)

        # Icono 96×96
        icon_paths = [
            "/usr/share/icons/debbie.svg",
            "/usr/share/icons/hicolor/scalable/apps/debbie.svg",
            os.path.join(os.path.dirname(__file__), "debbie.svg"),
        ]
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                pix_lbl = QLabel()
                pix = QPixmap(icon_path).scaled(
                    96, 96,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                pix_lbl.setPixmap(pix)
                pix_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(pix_lbl)
                break
        else:
            # Fallback: icono de tema
            fallback = QLabel()
            pm = QIcon.fromTheme("package-x-generic").pixmap(QSize(96, 96))
            fallback.setPixmap(pm)
            fallback.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback)

        # Nombre del programa
        name_lbl = QLabel("<b style='font-size:16pt'>Debbie</b>")
        name_lbl.setTextFormat(Qt.TextFormat.RichText)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_lbl)

        # Versión
        ver_lbl = QLabel("3.4")
        ver_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ver_lbl)

        # Descripción
        desc_lbl = QLabel(_("about_program"))
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl)

        # URL del sitio web
        website = "https://cuerdos.github.io"
        url_lbl = QLabel(f'<a href="{website}">{_("about_website")}</a>')
        url_lbl.setTextFormat(Qt.TextFormat.RichText)
        url_lbl.setOpenExternalLinks(True)
        url_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(url_lbl)

        # Copyright
        copy_lbl = QLabel("🄯 2026 CuerdOS — GPL-3.0")
        copy_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copy_lbl)

        layout.addSpacing(8)

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dlg.accept)
        layout.addWidget(ok_btn)

        dlg.exec()


# ═════════════════════════════════════════════════════════════════════════════
# Punto de entrada
# ═════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Debbie")
    app.setApplicationVersion("3.4")
    app.setOrganizationName("CuerdOS")
    app.setDesktopFileName("debbie")   # Wayland app_id

    app.setStyleSheet(STYLESHEET)

    input_file = None
    if len(sys.argv) > 1:
        candidate = sys.argv[1]
        if candidate.endswith('.deb') and os.path.exists(candidate):
            input_file = candidate

    window = DebInstaller(input_file)
    window.show()

    # Ocultar widgets que no deben mostrarse al inicio
    window.progress_bar.hide()
    window.remove_button.hide()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()