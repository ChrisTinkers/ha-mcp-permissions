# HA MCP Permissions – Installation (ungetesteter erster Build)

**Noch nicht installieren, bevor die Codeprüfung und die Sicherheits- und Funktionstests abgeschlossen sind.**

Der Dienst benötigt eine mindestens 32 Zeichen lange, zufällig erzeugte `access_key`-Zeichenfolge in den Home-Assistant-App-Optionen. Sie wird als geheimer Pfad im MCP-URL-Schema verwendet. Dieser Pfad ist ein Zugangsschlüssel: nicht teilen, nicht in Issues oder Chat kopieren.

Der standardmäßige Netzwerk-Port wird *nicht* auf den Host veröffentlicht (`8765/tcp: null`). Ein separater Tunnel-Container im Home-Assistant-App-Netzwerk könnte auf den internen Dienst zugreifen, nachdem sein Hostname ermittelt wurde. Das Vorhandensein des Zugangs darf nicht als Bestätigung der Schreibfähigkeit in ChatGPT ausgelegt werden.

**Wichtig:** `homeassistant_api: true` gibt dem Container technisch administrativen Home-Assistant-API-Zugang. Die Beschränkung auf die To-do-Liste wird durch die Anwendung erzwungen, nicht durch die Privilegien des Supervisor-Tokens. Eine kompromittierte Anwendung könnte daher prinzipiell mehr. Für strengste Isolation wäre ein API-Gateway mit tatsächlich begrenztem Backend-Credential nötig.

Vor Livebetrieb:
1. Code review, Abhängigkeiten pinnen, Integrationstest mit HA 2026.11.
2. Negativtests für andere Entitäten und Dienste.
3. Neuen separaten Tunnel konfigurieren und ChatGPT-Fähigkeiten testen.
4. Den bereits offengelegten API-Key ersetzen.
5. Erst danach Schreibaktionen nutzen.

Der vorhandene lesende MCP-Server und sein Tunnel bleiben unverändert.
