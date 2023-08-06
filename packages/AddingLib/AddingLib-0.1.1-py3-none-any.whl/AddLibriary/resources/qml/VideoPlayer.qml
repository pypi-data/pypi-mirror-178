import QtQuick 2.0
import ajax.plugin.video 1.0 as VideoPlugin
//import "qrc:/resources/qml/components/911/" as Custom
//import "qrc:/resources/qml/components/911/DS3" as DS3

import QtQuick.Layouts 1.13
import QtQuick.Controls 2.12

VideoPlugin.VideoPlayerWindow {
    anchors.fill: parent
    id: videoPlayer

    ColumnLayout{
        anchors.fill: parent
            RowLayout{
                Rectangle{
                }
        }
        RowLayout{
            spacing: 120
            Button {
                opacity: 0.5
                text: "Play"
                onClicked: videoPlayer.playbackController.play()
            }

            Button {
                opacity: 0.5
                text: "Pause"
                onClicked: videoPlayer.playbackController.pause()
            }
        }
    }


    Popup {
        id: popup 
        width: 150
        height: 150
        opacity: 0.5
        modal: true
        focus: true
        anchors.centerIn: videoPlayer
        contentItem: Text {
            text: "Content"
        }

        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    }

    Connections{
        target: videoPlayer.playbackController

        function onStatusChanged(message) {
            console.log("Status changed")
            popup.contentItem.text = message
            popup.open()
        }
    }
}