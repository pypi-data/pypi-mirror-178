import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12
import QtWebEngine 1.8

import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: popup
    width: application.width * 0.75
    height: application.height * 0.75

    Rectangle {
        id: mapBody
        anchors.fill: parent
        color: "#212121"
        clip: true

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        WebEngineView {
            id: webEngine
            anchors.fill: parent

            onLoadingChanged: {
                if (loadRequest.status == WebEngineView.LoadSucceededStatus) acceptButton.visible = true
            }
        }

        Rectangle {
            id: acceptButton
            width: 200
            height: 50
            color: "#212121"
            border.width: 3
            border.color: ui.colors.green1
            visible: false

            anchors {
                bottom: parent.bottom
                bottomMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            Text {
                font.family: roboto.name
                font.pixelSize: 16
                color: ui.colors.light1
                text: tr.confirm
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    webEngine.runJavaScript("get()", function(result) {
                        client.process_map_data(result)
                        popup.close()
                    })
                }
            }
        }
    }

    Component.onCompleted: {
        var information = {}
        information["lat"] = hub.latitude ? hub.latitude : "50.45466"
        information["lon"] = hub.longitude ? hub.longitude : "30.52380"

        var html = client.get_map_html(information, "address")
        webEngine.loadHtml(html)
    }
}
