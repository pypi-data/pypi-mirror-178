import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0
import QtWebEngine 1.8

import "qrc:/resources/qml/components/desktop/"

AjaxPopup {
    id: popup
    width: application.width * 0.7
    height: application.height * 0.68

    Rectangle {
        id: loginBody
        anchors.fill: parent
        color: "#212121"
        clip: true

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        WebEngineView {
            id: webEngine
            anchors.fill: parent
            url: ezviz.login_link
            zoomFactor: 0.9
            profile: WebEngineProfile { httpCacheType: WebEngineProfile.NoCache }

            onContextMenuRequested: {
                request.accepted = true
            }

            onUrlChanged: {
                if (url == ezviz.login_link) {
                    return
                }
                ezviz.save_login_data(url)
                popup.close()
            }

            onLoadingChanged: {
                webEngine.runJavaScript("var el = document.getElementById('registBtn'); if (el) { el.outerHTML = '' };")
            }
        }
    }
}
