import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12
import QtWebEngine 1.8

AjaxPopup {
    id: popup
    width: application.width * 0.7
    height: application.height * 0.7

    property var information: null
    property var mode: "panic"
    // {"location":{"lat":50.4939907,"lon":30.4680436,"acc":17.218,"speed":0.0,"time":1555501922}}

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
                    var lat = result.data.lat.toString(10).split(".")
                    lat[1] = lat[1].slice(0,6)
                    var lng = result.data.lng.toString(10).split(".")
                    lng[1] = lng[1].slice(0,6)
                    var coordinates = ''.concat(lat[0], ".", lat[1], ", ", lng[0], ".", lng[1])
                    locationField.value = coordinates
//                    client.process_map_data(result)
                    popup.close()
                    })
                }
            }
        }
    }

    Component.onCompleted: {
        var html = app.get_map_html(information, mode)
        webEngine.loadHtml(html)
    }
}