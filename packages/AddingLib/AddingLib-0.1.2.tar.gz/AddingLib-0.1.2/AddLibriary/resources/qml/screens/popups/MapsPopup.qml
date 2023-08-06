import QtQuick 2.12
import QtQuick.Controls 2.2
import QtWebEngine 1.8

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    property var info: null

    function round(value) {
        return Math.round(value * 100000000) / 100000000
    }

    Component.onCompleted: {
        if (popup.info.mode == "address") {
            var information = {}
            information["lat"] = popup.info.info.lat ? popup.info.info.lat : "50.45466"
            information["lon"] = popup.info.info.lon ? popup.info.info.lon : "30.52380"

            var html = app.get_map_html(information, popup.info.mode)
            webEngine.loadHtml(html)
        } else {
            var html = app.get_map_html(popup.info.info, popup.info.mode)
            webEngine.loadHtml(html)
        }
    }

    width: 670
    height: 650

    sideMargins: 0

    header: DS3.NavBarModal {
        headerText: tr.coordinates
    }

    footer: Item {
        width: parent.width
        height: 0
    }

    DS3.Spacing {
        height: 24
    }

    Item {
        id: container

        width: popup.width - 48
        height: popup.height - 200

        anchors.horizontalCenter: parent.horizontalCenter

        WebEngineView {
            id: webEngine

            anchors.fill: parent

            onLoadingChanged: {
                if (popup.info.mode != "address") return

                if (loadRequest.status == WebEngineView.LoadSucceededStatus) confirmButton.visible = true
            }
        }

         Item {
            // transparent layer to catch a click over the map

            anchors.fill: webEngine

            MouseArea {
                anchors.fill: parent
                propagateComposedEvents: true

                onPressed: {
                    confirmButton.enabled = true
                    mouse.accepted = false
                }
            }
        }
    }

    DS3.Spacing {
        height: 32
    }

    DS3.ButtonBar {
        id: confirmButton

        anchors.horizontalCenter: parent.horizontalCenter

        buttonText: tr.confirm
        visible: false
        enabled: false

        button.onClicked: {
            webEngine.runJavaScript("get()", function(result) {
                app.process_map_data(result)
                popup.close()
            })
        }
    }
}