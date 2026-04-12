import os
import locale as _locale

def _detect_system_language():
    """
    Detecta el idioma del sistema operativo al arrancar.
    Devuelve un código soportado o 'en' como fallback seguro.
    """
    supported = {"es", "en", "pt", "it", "de", "ja", "ko", "ca"}

    for env_var in ("LANGUAGE", "LANG", "LC_ALL", "LC_MESSAGES"):
        val = os.environ.get(env_var, "")
        # LANGUAGE puede ser una lista separada por ':' (ej: "es:en")
        for entry in val.split(":"):
            code = entry.split("_")[0].split(".")[0].lower().strip()
            if code and code != "c" and code in supported:
                return code

    # Fallback: locale del sistema via módulo locale
    try:
        loc = _locale.getlocale()[0] or ""
        code = loc.split("_")[0].lower()
        if code in supported:
            return code
    except Exception:
        pass

    return "en"  # Fallback final neutral

current_language = _detect_system_language()

translations = {
    "en": {
        # Window and UI
        "title": "Debbie Package Installer",
        "drop_deb_here": "Drop .deb file here",
        "or_click_to_open": "or click to open",
        "no_file": "No file selected",
        "ready": "Ready",

        # File operations
        "file": "File",
        "loaded": "Loaded",
        "package": "Package",
        "version": "Version",
        "size": "Size",
        "architecture": "Architecture",
        "unknown": "Unknown",
        "file_not_found": "File not found",
        "failed_to_load_package_info": "Failed to load package information",
        "not_deb_file": "This is not a .deb file",

        # Buttons and actions
        "open_deb": "Open .deb file",
        "extract_package": "Extract package",
        "change_language": "Change language",
        "about": "About",
        "install": "Install",
        "upgrade": "Upgrade",
        "update": "Update",
        "downgrade": "Downgrade",
        "reinstall": "Reinstall",
        "remove": "Remove",
        "cancel": "Cancel",
        "verify_package": "Verify package",
        "select_language": "Select Language",

        # Package information
        "package_information": "Package Information",
        "installation_output": "Installation Output",
        "not_installed": "Not installed",
        "upgrade_available": "Upgrade available",
        "downgrade_warning": "Downgrade warning",
        "same_version_installed": "Same version installed",
        "installed_version": "Installed version",
        "deb_version": "DEB version",
        "update_available": "Update available",
        "older_version_detected": "Older version detected",
        "same_version": "Same version",
        "installed": "Installed",
        "new": "New",

        # Dialogs and messages
        "error": "Error",
        "success": "Success",
        "loading_package": "Loading package information...",
        "running_command": "Running command...",
        "package_installed_successfully": "Package installed successfully",
        "package_removed_successfully": "Package removed successfully",
        "process_cancelled": "Process cancelled",
        "process_already_running": "A process is already running",
        "command_error": "Command error",
        "cancel_error": "Cancel error",
        "installation_failed": "Installation failed",
        "removal_failed": "Removal failed",
        "unexpected_error": "Unexpected error",
        "operation_failed": "Operation failed",
        "authentication_failed": "Authentication failed",

        # Confirmations
        "confirm_install": "Install package",
        "confirm_remove": "Remove package",
        "confirm_uninstall": "Confirm package removal",

        # Process messages
        "installing": "Installing",
        "removing": "Removing",

        # File dialogs
        "select_deb_file": "Select .deb file",
        "select_deb_package": "Select .deb package",
        "select_extraction_folder": "Select extraction folder",
        "select_extract_directory": "Select extraction directory",
        "deb_packages": "DEB packages",
        "deb_files": "DEB files (*.deb)",
        "invalid_deb_file": "Invalid .deb file",
        "no_package_loaded": "No package loaded",

        # Package operations
        "no_package_selected": "No package selected",
        "cannot_determine_package": "Cannot determine package name",
        "cannot_get_package_info": "Cannot get package information",
        "package_extracted_to": "Package extracted to",
        "extraction_failed": "Extraction failed",

        # Verification
        "package_verification_passed": "Package verification passed",
        "package_verification_failed": "Package verification failed",
        "package_structure": "Package structure",
        "format_validation": "Format validation",
        "verification_results": "Verification Results",

        # About dialog
        "about_program": "A modern .deb package installer with drag & drop support",
        "about_website": "Visit website"
    },

    "es": {
        # Window and UI
        "title": "Instalador de Paquetes Debbie",
        "drop_deb_here": "Arrastra el archivo .deb aquí",
        "or_click_to_open": "o haz clic para abrir",
        "no_file": "Ningún archivo seleccionado",
        "ready": "Listo",

        # File operations
        "file": "Archivo",
        "loaded": "Cargado",
        "package": "Paquete",
        "version": "Versión",
        "size": "Tamaño",
        "architecture": "Arquitectura",
        "unknown": "Desconocido",
        "file_not_found": "Archivo no encontrado",
        "failed_to_load_package_info": "Error al cargar la información del paquete",
        "not_deb_file": "Este no es un archivo .deb",

        # Buttons and actions
        "open_deb": "Abrir archivo .deb",
        "extract_package": "Extraer paquete",
        "change_language": "Cambiar idioma",
        "about": "Acerca de",
        "install": "Instalar",
        "upgrade": "Actualizar",
        "update": "Actualizar",
        "downgrade": "Desactualizar",
        "reinstall": "Reinstalar",
        "remove": "Eliminar",
        "cancel": "Cancelar",
        "verify_package": "Verificar paquete",
        "select_language": "Seleccionar Idioma",

        # Package information
        "package_information": "Información del Paquete",
        "installation_output": "Salida de Instalación",
        "not_installed": "No instalado",
        "upgrade_available": "Actualización disponible",
        "downgrade_warning": "Advertencia de desactualización",
        "same_version_installed": "Misma versión instalada",
        "installed_version": "Versión instalada",
        "deb_version": "Versión DEB",
        "update_available": "Actualización disponible",
        "older_version_detected": "Versión anterior detectada",
        "same_version": "Misma versión",
        "installed": "Instalado",
        "new": "Nuevo",

        # Dialogs and messages
        "error": "Error",
        "success": "Éxito",
        "loading_package": "Cargando información del paquete...",
        "running_command": "Ejecutando comando...",
        "package_installed_successfully": "Paquete instalado exitosamente",
        "package_removed_successfully": "Paquete eliminado exitosamente",
        "process_cancelled": "Proceso cancelado",
        "process_already_running": "Ya hay un proceso en ejecución",
        "command_error": "Error de comando",
        "cancel_error": "Error de cancelación",
        "installation_failed": "La instalación falló",
        "removal_failed": "La eliminación falló",
        "unexpected_error": "Error inesperado",
        "operation_failed": "Operación fallida",
        "authentication_failed": "Autenticación fallida",

        # Confirmations
        "confirm_install": "¿Instalar paquete",
        "confirm_remove": "¿Eliminar paquete",
        "confirm_uninstall": "Confirmar eliminación del paquete",

        # Process messages
        "installing": "Instalando",
        "removing": "Eliminando",

        # File dialogs
        "select_deb_file": "Seleccionar archivo .deb",
        "select_deb_package": "Seleccionar paquete .deb",
        "select_extraction_folder": "Seleccionar carpeta de extracción",
        "select_extract_directory": "Seleccionar directorio de extracción",
        "deb_packages": "Paquetes DEB",
        "deb_files": "Archivos DEB (*.deb)",
        "invalid_deb_file": "Archivo .deb inválido",
        "no_package_loaded": "Ningún paquete cargado",

        # Package operations
        "no_package_selected": "Ningún paquete seleccionado",
        "cannot_determine_package": "No se puede determinar el nombre del paquete",
        "cannot_get_package_info": "No se puede obtener información del paquete",
        "package_extracted_to": "Paquete extraído en",
        "extraction_failed": "Falló la extracción",

        # Verification
        "package_verification_passed": "Verificación del paquete exitosa",
        "package_verification_failed": "Falló la verificación del paquete",
        "package_structure": "Estructura del paquete",
        "format_validation": "Validación de formato",
        "verification_results": "Resultados de Verificación",

        # About dialog
        "about_program": "Un instalador moderno de paquetes .deb con soporte de arrastrar y soltar",
        "about_website": "Visitar sitio web"
    },

    "pt": {
        # Window and UI
        "title": "Instalador de Pacotes Debbie",
        "drop_deb_here": "Arraste o arquivo .deb para cá",
        "or_click_to_open": "ou clique para abrir",
        "no_file": "Nenhum arquivo selecionado",
        "ready": "Pronto",

        # File operations
        "file": "Arquivo",
        "loaded": "Carregado",
        "package": "Pacote",
        "version": "Versão",
        "size": "Tamanho",
        "architecture": "Arquitetura",
        "unknown": "Desconhecido",
        "file_not_found": "Arquivo não encontrado",
        "failed_to_load_package_info": "Falha ao carregar informações do pacote",
        "not_deb_file": "Este não é um arquivo .deb",

        # Buttons and actions
        "open_deb": "Abrir arquivo .deb",
        "extract_package": "Extrair pacote",
        "change_language": "Mudar idioma",
        "about": "Sobre",
        "install": "Instalar",
        "upgrade": "Atualizar",
        "update": "Atualizar",
        "downgrade": "Fazer downgrade",
        "reinstall": "Reinstalar",
        "remove": "Remover",
        "cancel": "Cancelar",
        "verify_package": "Verificar pacote",
        "select_language": "Selecionar Idioma",

        # Package information
        "package_information": "Informações do Pacote",
        "installation_output": "Saída da Instalação",
        "not_installed": "Não instalado",
        "upgrade_available": "Atualização disponível",
        "downgrade_warning": "Aviso de downgrade",
        "same_version_installed": "Mesma versão instalada",
        "installed_version": "Versão instalada",
        "deb_version": "Versão DEB",
        "update_available": "Atualização disponível",
        "older_version_detected": "Versão mais antiga detectada",
        "same_version": "Mesma versão",
        "installed": "Instalado",
        "new": "Novo",

        # Dialogs and messages
        "error": "Erro",
        "success": "Sucesso",
        "loading_package": "Carregando informações do pacote...",
        "running_command": "Executando comando...",
        "package_installed_successfully": "Pacote instalado com sucesso",
        "package_removed_successfully": "Pacote removido com sucesso",
        "process_cancelled": "Processo cancelado",
        "process_already_running": "Já existe um processo em execução",
        "command_error": "Erro de comando",
        "cancel_error": "Erro de cancelamento",
        "installation_failed": "Instalação falhou",
        "removal_failed": "Remoção falhou",
        "unexpected_error": "Erro inesperado",
        "operation_failed": "Operação falhou",
        "authentication_failed": "Autenticação falhou",

        # Confirmations
        "confirm_install": "Instalar pacote",
        "confirm_remove": "Remover pacote",
        "confirm_uninstall": "Confirmar remoção do pacote",

        # Process messages
        "installing": "Instalando",
        "removing": "Removendo",

        # File dialogs
        "select_deb_file": "Selecionar arquivo .deb",
        "select_deb_package": "Selecionar pacote .deb",
        "select_extraction_folder": "Selecionar pasta de extração",
        "select_extract_directory": "Selecionar diretório de extração",
        "deb_packages": "Pacotes DEB",
        "deb_files": "Arquivos DEB (*.deb)",
        "invalid_deb_file": "Arquivo .deb inválido",
        "no_package_loaded": "Nenhum pacote carregado",

        # Package operations
        "no_package_selected": "Nenhum pacote selecionado",
        "cannot_determine_package": "Não é possível determinar o nome do pacote",
        "cannot_get_package_info": "Não é possível obter informações do pacote",
        "package_extracted_to": "Pacote extraído para",
        "extraction_failed": "Extração falhou",

        # Verification
        "package_verification_passed": "Verificação do pacote bem-sucedida",
        "package_verification_failed": "Verificação do pacote falhou",
        "package_structure": "Estrutura do pacote",
        "format_validation": "Validação de formato",
        "verification_results": "Resultados da Verificação",

        # About dialog
        "about_program": "Um instalador moderno de pacotes .deb com suporte de arrastar e soltar",
        "about_website": "Visitar site"
    },

    "de": {
        # Window and UI
        "title": "Debbie Paketinstaller",
        "drop_deb_here": ".deb-Datei hier ablegen",
        "or_click_to_open": "oder klicken zum Öffnen",
        "no_file": "Keine Datei ausgewählt",
        "ready": "Bereit",

        # File operations
        "file": "Datei",
        "loaded": "Geladen",
        "package": "Paket",
        "version": "Version",
        "size": "Größe",
        "architecture": "Architektur",
        "unknown": "Unbekannt",
        "file_not_found": "Datei nicht gefunden",
        "failed_to_load_package_info": "Fehler beim Laden der Paketinformationen",
        "not_deb_file": "Dies ist keine .deb-Datei",

        # Buttons and actions
        "open_deb": ".deb-Datei öffnen",
        "extract_package": "Paket extrahieren",
        "change_language": "Sprache ändern",
        "about": "Über",
        "install": "Installieren",
        "upgrade": "Aktualisieren",
        "update": "Aktualisieren",
        "downgrade": "Herabstufen",
        "reinstall": "Neu installieren",
        "remove": "Entfernen",
        "cancel": "Abbrechen",
        "verify_package": "Paket überprüfen",
        "select_language": "Sprache auswählen",

        # Package information
        "package_information": "Paketinformationen",
        "installation_output": "Installationsausgabe",
        "not_installed": "Nicht installiert",
        "upgrade_available": "Aktualisierung verfügbar",
        "downgrade_warning": "Downgrade-Warnung",
        "same_version_installed": "Gleiche Version installiert",
        "installed_version": "Installierte Version",
        "deb_version": "DEB-Version",
        "update_available": "Aktualisierung verfügbar",
        "older_version_detected": "Ältere Version erkannt",
        "same_version": "Gleiche Version",
        "installed": "Installiert",
        "new": "Neu",

        # Dialogs and messages
        "error": "Fehler",
        "success": "Erfolg",
        "loading_package": "Paketinformationen werden geladen...",
        "running_command": "Befehl wird ausgeführt...",
        "package_installed_successfully": "Paket erfolgreich installiert",
        "package_removed_successfully": "Paket erfolgreich entfernt",
        "process_cancelled": "Vorgang abgebrochen",
        "process_already_running": "Es läuft bereits ein Prozess",
        "command_error": "Befehlsfehler",
        "cancel_error": "Abbruchfehler",
        "installation_failed": "Installation fehlgeschlagen",
        "removal_failed": "Entfernung fehlgeschlagen",
        "unexpected_error": "Unerwarteter Fehler",
        "operation_failed": "Operation fehlgeschlagen",
        "authentication_failed": "Authentifizierung fehlgeschlagen",

        # Confirmations
        "confirm_install": "Paket installieren",
        "confirm_remove": "Paket entfernen",
        "confirm_uninstall": "Paketentfernung bestätigen",

        # Process messages
        "installing": "Installieren",
        "removing": "Entfernen",

        # File dialogs
        "select_deb_file": ".deb-Datei auswählen",
        "select_deb_package": ".deb-Paket auswählen",
        "select_extraction_folder": "Extraktionsordner auswählen",
        "select_extract_directory": "Extraktionsverzeichnis auswählen",
        "deb_packages": "DEB-Pakete",
        "deb_files": "DEB-Dateien (*.deb)",
        "invalid_deb_file": "Ungültige .deb-Datei",
        "no_package_loaded": "Kein Paket geladen",

        # Package operations
        "no_package_selected": "Kein Paket ausgewählt",
        "cannot_determine_package": "Paketname kann nicht bestimmt werden",
        "cannot_get_package_info": "Paketinformationen können nicht abgerufen werden",
        "package_extracted_to": "Paket extrahiert nach",
        "extraction_failed": "Extraktion fehlgeschlagen",

        # Verification
        "package_verification_passed": "Paketüberprüfung erfolgreich",
        "package_verification_failed": "Paketüberprüfung fehlgeschlagen",
        "package_structure": "Paketstruktur",
        "format_validation": "Formatvalidierung",
        "verification_results": "Überprüfungsergebnisse",

        # About dialog
        "about_program": "Ein moderner .deb-Paketinstaller mit Drag & Drop-Unterstützung",
        "about_website": "Website besuchen"
    },

    "it": {
        # Window and UI
        "title": "Installatore Pacchetti Debbie",
        "drop_deb_here": "Trascina il file .deb qui",
        "or_click_to_open": "o clicca per aprire",
        "no_file": "Nessun file selezionato",
        "ready": "Pronto",

        # File operations
        "file": "File",
        "loaded": "Caricato",
        "package": "Pacchetto",
        "version": "Versione",
        "size": "Dimensione",
        "architecture": "Architettura",
        "unknown": "Sconosciuto",
        "file_not_found": "File non trovato",
        "failed_to_load_package_info": "Impossibile caricare le informazioni del pacchetto",
        "not_deb_file": "Questo non è un file .deb",

        # Buttons and actions
        "open_deb": "Apri file .deb",
        "extract_package": "Estrai pacchetto",
        "change_language": "Cambia lingua",
        "about": "Informazioni",
        "install": "Installa",
        "upgrade": "Aggiorna",
        "update": "Aggiorna",
        "downgrade": "Retrocedi",
        "reinstall": "Reinstalla",
        "remove": "Rimuovi",
        "cancel": "Annulla",
        "verify_package": "Verifica pacchetto",
        "select_language": "Seleziona Lingua",

        # Package information
        "package_information": "Informazioni Pacchetto",
        "installation_output": "Output Installazione",
        "not_installed": "Non installato",
        "upgrade_available": "Aggiornamento disponibile",
        "downgrade_warning": "Avviso downgrade",
        "same_version_installed": "Stessa versione installata",
        "installed_version": "Versione installata",
        "deb_version": "Versione DEB",
        "update_available": "Aggiornamento disponibile",
        "older_version_detected": "Versione precedente rilevata",
        "same_version": "Stessa versione",
        "installed": "Installato",
        "new": "Nuovo",

        # Dialogs and messages
        "error": "Errore",
        "success": "Successo",
        "loading_package": "Caricamento informazioni pacchetto...",
        "running_command": "Esecuzione comando...",
        "package_installed_successfully": "Pacchetto installato con successo",
        "package_removed_successfully": "Pacchetto rimosso con successo",
        "process_cancelled": "Processo annullato",
        "process_already_running": "Un processo è già in esecuzione",
        "command_error": "Errore comando",
        "cancel_error": "Errore annullamento",
        "installation_failed": "Installazione fallita",
        "removal_failed": "Rimozione fallita",
        "unexpected_error": "Errore imprevisto",
        "operation_failed": "Operazione fallita",
        "authentication_failed": "Autenticazione fallita",

        # Confirmations
        "confirm_install": "Installare pacchetto",
        "confirm_remove": "Rimuovere pacchetto",
        "confirm_uninstall": "Conferma rimozione pacchetto",

        # Process messages
        "installing": "Installazione",
        "removing": "Rimozione",

        # File dialogs
        "select_deb_file": "Seleziona file .deb",
        "select_deb_package": "Seleziona pacchetto .deb",
        "select_extraction_folder": "Seleziona cartella di estrazione",
        "select_extract_directory": "Seleziona directory di estrazione",
        "deb_packages": "Pacchetti DEB",
        "deb_files": "File DEB (*.deb)",
        "invalid_deb_file": "File .deb non valido",
        "no_package_loaded": "Nessun pacchetto caricato",

        # Package operations
        "no_package_selected": "Nessun pacchetto selezionato",
        "cannot_determine_package": "Impossibile determinare il nome del pacchetto",
        "cannot_get_package_info": "Impossibile ottenere informazioni del pacchetto",
        "package_extracted_to": "Pacchetto estratto in",
        "extraction_failed": "Estrazione fallita",

        # Verification
        "package_verification_passed": "Verifica pacchetto riuscita",
        "package_verification_failed": "Verifica pacchetto fallita",
        "package_structure": "Struttura pacchetto",
        "format_validation": "Validazione formato",
        "verification_results": "Risultati Verifica",

        # About dialog
        "about_program": "Un moderno installatore di pacchetti .deb con supporto drag & drop",
        "about_website": "Visita sito web"
    },

    "ca": {
        # Window and UI
        "title": "Instal·lador de Paquets Debbie",
        "drop_deb_here": "Deixa anar el fitxer .deb aquí",
        "or_click_to_open": "o fes clic per obrir",
        "no_file": "Cap fitxer seleccionat",
        "ready": "A punt",

        # File operations
        "file": "Fitxer",
        "loaded": "Carregat",
        "package": "Paquet",
        "version": "Versió",
        "size": "Mida",
        "architecture": "Arquitectura",
        "unknown": "Desconegut",
        "file_not_found": "Fitxer no trobat",
        "failed_to_load_package_info": "Error en carregar la informació del paquet",
        "not_deb_file": "Aquest no és un fitxer .deb",

        # Buttons and actions
        "open_deb": "Obrir fitxer .deb",
        "extract_package": "Extreure paquet",
        "change_language": "Canviar idioma",
        "about": "Quant a",
        "install": "Instal·lar",
        "upgrade": "Actualitzar",
        "update": "Actualitzar",
        "downgrade": "Degradar",
        "reinstall": "Reinstal·lar",
        "remove": "Eliminar",
        "cancel": "Cancel·lar",
        "verify_package": "Verificar paquet",
        "select_language": "Seleccionar Idioma",

        # Package information
        "package_information": "Informació del Paquet",
        "installation_output": "Sortida d'Instal·lació",
        "not_installed": "No instal·lat",
        "upgrade_available": "Actualització disponible",
        "downgrade_warning": "Avís de degradació",
        "same_version_installed": "Mateixa versió instal·lada",
        "installed_version": "Versió instal·lada",
        "deb_version": "Versió DEB",
        "update_available": "Actualització disponible",
        "older_version_detected": "Versió anterior detectada",
        "same_version": "Mateixa versió",
        "installed": "Instal·lat",
        "new": "Nou",

        # Dialogs and messages
        "error": "Error",
        "success": "Èxit",
        "loading_package": "S'està carregant la informació del paquet...",
        "running_command": "S'està executant la comanda...",
        "package_installed_successfully": "Paquet instal·lat correctament",
        "package_removed_successfully": "Paquet eliminat correctament",
        "process_cancelled": "Procés cancel·lat",
        "process_already_running": "Ja hi ha un procés en execució",
        "command_error": "Error de comanda",
        "cancel_error": "Error de cancel·lació",
        "installation_failed": "La instal·lació ha fallat",
        "removal_failed": "L'eliminació ha fallat",
        "unexpected_error": "Error inesperat",
        "operation_failed": "Operació fallida",
        "authentication_failed": "Autenticació fallida",

        # Confirmations
        "confirm_install": "Instal·lar paquet",
        "confirm_remove": "Eliminar paquet",
        "confirm_uninstall": "Confirmar eliminació del paquet",

        # Process messages
        "installing": "Instal·lant",
        "removing": "Eliminant",

        # File dialogs
        "select_deb_file": "Seleccionar fitxer .deb",
        "select_deb_package": "Seleccionar paquet .deb",
        "select_extraction_folder": "Seleccionar carpeta d'extracció",
        "select_extract_directory": "Seleccionar directori d'extracció",
        "deb_packages": "Paquets DEB",
        "deb_files": "Fitxers DEB (*.deb)",
        "invalid_deb_file": "Fitxer .deb invàlid",
        "no_package_loaded": "Cap paquet carregat",

        # Package operations
        "no_package_selected": "Cap paquet seleccionat",
        "cannot_determine_package": "No es pot determinar el nom del paquet",
        "cannot_get_package_info": "No es pot obtenir informació del paquet",
        "package_extracted_to": "Paquet extret a",
        "extraction_failed": "Ha fallat l'extracció",

        # Verification
        "package_verification_passed": "Verificació del paquet superada",
        "package_verification_failed": "Ha fallat la verificació del paquet",
        "package_structure": "Estructura del paquet",
        "format_validation": "Validació de format",
        "verification_results": "Resultats de Verificació",

        # About dialog
        "about_program": "Un instal·lador modern de paquets .deb amb suport arrossegar i deixar anar",
        "about_website": "Visitar lloc web"
    },

    "ja": {
        # Window and UI
        "title": "Debbieパッケージインストーラー",
        "drop_deb_here": ".debファイルをここにドロップ",
        "or_click_to_open": "またはクリックして開く",
        "no_file": "ファイルが選択されていません",
        "ready": "準備完了",

        # File operations
        "file": "ファイル",
        "loaded": "読み込み済み",
        "package": "パッケージ",
        "version": "バージョン",
        "size": "サイズ",
        "architecture": "アーキテクチャ",
        "unknown": "不明",
        "file_not_found": "ファイルが見つかりません",
        "failed_to_load_package_info": "パッケージ情報の読み込みに失敗しました",
        "not_deb_file": "これは.debファイルではありません",

        # Buttons and actions
        "open_deb": ".debファイルを開く",
        "extract_package": "パッケージを抽出",
        "change_language": "言語を変更",
        "about": "について",
        "install": "インストール",
        "upgrade": "アップグレード",
        "update": "アップデート",
        "downgrade": "ダウングレード",
        "reinstall": "再インストール",
        "remove": "削除",
        "cancel": "キャンセル",
        "verify_package": "パッケージを検証",
        "select_language": "言語を選択",

        # Package information
        "package_information": "パッケージ情報",
        "installation_output": "インストール出力",
        "not_installed": "未インストール",
        "upgrade_available": "アップグレード可能",
        "downgrade_warning": "ダウングレード警告",
        "same_version_installed": "同じバージョンがインストール済み",
        "installed_version": "インストール済みバージョン",
        "deb_version": "DEBバージョン",
        "update_available": "アップデート可能",
        "older_version_detected": "旧バージョンを検出",
        "same_version": "同じバージョン",
        "installed": "インストール済み",
        "new": "新しい",

        # Dialogs and messages
        "error": "エラー",
        "success": "成功",
        "loading_package": "パッケージ情報を読み込み中...",
        "running_command": "コマンドを実行中...",
        "package_installed_successfully": "パッケージのインストールに成功しました",
        "package_removed_successfully": "パッケージの削除に成功しました",
        "process_cancelled": "プロセスがキャンセルされました",
        "process_already_running": "既にプロセスが実行中です",
        "command_error": "コマンドエラー",
        "cancel_error": "キャンセルエラー",
        "installation_failed": "インストールに失敗しました",
        "removal_failed": "削除に失敗しました",
        "unexpected_error": "予期しないエラー",
        "operation_failed": "操作に失敗しました",
        "authentication_failed": "認証に失敗しました",

        # Confirmations
        "confirm_install": "パッケージをインストール",
        "confirm_remove": "パッケージを削除",
        "confirm_uninstall": "パッケージの削除を確認",

        # Process messages
        "installing": "インストール中",
        "removing": "削除中",

        # File dialogs
        "select_deb_file": ".debファイルを選択",
        "select_deb_package": ".debパッケージを選択",
        "select_extraction_folder": "抽出フォルダーを選択",
        "select_extract_directory": "抽出ディレクトリを選択",
        "deb_packages": "DEBパッケージ",
        "deb_files": "DEBファイル (*.deb)",
        "invalid_deb_file": "無効な.debファイル",
        "no_package_loaded": "パッケージが読み込まれていません",

        # Package operations
        "no_package_selected": "パッケージが選択されていません",
        "cannot_determine_package": "パッケージ名を特定できません",
        "cannot_get_package_info": "パッケージ情報を取得できません",
        "package_extracted_to": "パッケージの抽出先",
        "extraction_failed": "抽出に失敗しました",

        # Verification
        "package_verification_passed": "パッケージの検証に成功しました",
        "package_verification_failed": "パッケージの検証に失敗しました",
        "package_structure": "パッケージ構造",
        "format_validation": "フォーマット検証",
        "verification_results": "検証結果",

        # About dialog
        "about_program": "ドラッグ&ドロップをサポートするモダンな.debパッケージインストーラー",
        "about_website": "ウェブサイトを訪問"
    },

    "ko": {
        # Window and UI
        "title": "Debbie 패키지 설치 프로그램",
        "drop_deb_here": ".deb 파일을 여기에 드롭하세요",
        "or_click_to_open": "또는 클릭하여 열기",
        "no_file": "선택된 파일 없음",
        "ready": "준비",

        # File operations
        "file": "파일",
        "loaded": "로드됨",
        "package": "패키지",
        "version": "버전",
        "size": "크기",
        "architecture": "아키텍처",
        "unknown": "알 수 없음",
        "file_not_found": "파일을 찾을 수 없음",
        "failed_to_load_package_info": "패키지 정보 로드 실패",
        "not_deb_file": ".deb 파일이 아닙니다",

        # Buttons and actions
        "open_deb": ".deb 파일 열기",
        "extract_package": "패키지 추출",
        "change_language": "언어 변경",
        "about": "정보",
        "install": "설치",
        "upgrade": "업그레이드",
        "update": "업데이트",
        "downgrade": "다운그레이드",
        "reinstall": "재설치",
        "remove": "제거",
        "cancel": "취소",
        "verify_package": "패키지 확인",
        "select_language": "언어 선택",

        # Package information
        "package_information": "패키지 정보",
        "installation_output": "설치 출력",
        "not_installed": "설치되지 않음",
        "upgrade_available": "업그레이드 가능",
        "downgrade_warning": "다운그레이드 경고",
        "same_version_installed": "같은 버전 설치됨",
        "installed_version": "설치된 버전",
        "deb_version": "DEB 버전",
        "update_available": "업데이트 가능",
        "older_version_detected": "이전 버전 감지됨",
        "same_version": "같은 버전",
        "installed": "설치됨",
        "new": "새로운",

        # Dialogs and messages
        "error": "오류",
        "success": "성공",
        "loading_package": "패키지 정보를 로드하는 중...",
        "running_command": "명령 실행 중...",
        "package_installed_successfully": "패키지가 성공적으로 설치되었습니다",
        "package_removed_successfully": "패키지가 성공적으로 제거되었습니다",
        "process_cancelled": "프로세스 취소됨",
        "process_already_running": "이미 프로세스가 실행 중입니다",
        "command_error": "명령 오류",
        "cancel_error": "취소 오류",
        "installation_failed": "설치 실패",
        "removal_failed": "제거 실패",
        "unexpected_error": "예기치 않은 오류",
        "operation_failed": "작업 실패",
        "authentication_failed": "인증 실패",

        # Confirmations
        "confirm_install": "패키지 설치",
        "confirm_remove": "패키지 제거",
        "confirm_uninstall": "패키지 제거 확인",

        # Process messages
        "installing": "설치 중",
        "removing": "제거 중",

        # File dialogs
        "select_deb_file": ".deb 파일 선택",
        "select_deb_package": ".deb 패키지 선택",
        "select_extraction_folder": "추출 폴더 선택",
        "select_extract_directory": "추출 디렉토리 선택",
        "deb_packages": "DEB 패키지",
        "deb_files": "DEB 파일 (*.deb)",
        "invalid_deb_file": "잘못된 .deb 파일",
        "no_package_loaded": "로드된 패키지 없음",

        # Package operations
        "no_package_selected": "선택된 패키지 없음",
        "cannot_determine_package": "패키지 이름을 확인할 수 없음",
        "cannot_get_package_info": "패키지 정보를 가져올 수 없음",
        "package_extracted_to": "패키지 추출 위치",
        "extraction_failed": "추출 실패",

        # Verification
        "package_verification_passed": "패키지 확인 성공",
        "package_verification_failed": "패키지 확인 실패",
        "package_structure": "패키지 구조",
        "format_validation": "형식 검증",
        "verification_results": "확인 결과",

        # About dialog
        "about_program": "드래그 앤 드롭을 지원하는 최신 .deb 패키지 설치 프로그램",
        "about_website": "웹사이트 방문"
    }
}

def _(key):
    """Get translation for current language"""
    return translations.get(current_language, translations["en"]).get(key, key)

def set_language(lang_code):
    """Set current language"""
    global current_language
    if lang_code in translations:
        current_language = lang_code