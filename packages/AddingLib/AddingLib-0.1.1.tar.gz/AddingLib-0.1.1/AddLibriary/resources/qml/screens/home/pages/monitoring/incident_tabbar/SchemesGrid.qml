import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


GridView {
    id: schemesGridView
    clip: true
    currentIndex: -1
    model: incident.proxy_facility_media

    cellWidth: (parent.width - parent.width % 4) / 4
    cellHeight: 144

    property var popupOpened: false

    delegate: Item {
        width: schemesGridView.cellWidth
        height: schemesGridView.cellHeight

        property var schemeUrl: url
        property var schemeCaption: media.caption

        Rectangle {
            anchors.fill: parent
            color: {
                if (currentIndex == index) return ui.colors.green3
                if (schemeArea.containsMouse) return ui.colors.dark2
                return "transparent"
            }
        }

        Item {
            id: schemeImageItem
            width: 112
            height: 112
            anchors {
                top: parent.top
                topMargin: 4
                horizontalCenter: parent.horizontalCenter
            }

            Image {
                fillMode: Image.PreserveAspectFit
                source: url ? url["128x128"] : ""
                anchors.fill: parent
            }
        }

        Item {
            width: parent.width
            anchors {
                top: schemeImageItem.bottom
                topMargin: 4
                bottom: parent.bottom
                bottomMargin: 4
            }

            Custom.FontText {
                text: media ? media.caption : ""
                width: parent.width - 8
                height: contentHeight
                anchors.centerIn: parent
                color: currentIndex == index ? ui.colors.dark3 : ui.colors.light3
                font.pixelSize: 12
                maximumLineCount: 1
                elide: Text.ElideRight
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Custom.HandMouseArea {
            id: schemeArea
            hoverEnabled: true

            onClicked: {
                schemesGridView.currentIndex = index
                if (schemesGridView.popupOpened) return
                schemesGridView.popupOpened = true
                Popups.scheme_image_popup(schemesGridView, topLevel)
            }
        }
    }

    Component.onCompleted: {
       app.facility_media_module.start_incident_facility_media_stream(incident)
    }

    Connections {
        target: schemesGridView.model

        onLengthChanged: {
            schemesGridView.currentIndex = -1
        }
    }
}