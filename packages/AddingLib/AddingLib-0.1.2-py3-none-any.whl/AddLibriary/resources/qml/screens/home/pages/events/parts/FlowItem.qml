import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: rectDelegate

    width: 72
    height: 32
    radius: height / 2
    color: ui.colors.dark4

    property alias mouseArea: mouseArea

    Loader {
        anchors.centerIn: parent
        sourceComponent: {
            switch(modelData.itemType) {
                case "Text": return textComponent
                case "Image": return imageComponent
            }
        }
    }

    Component {
        id: textComponent

        Custom.FontText {
            id: itemText

            width: 264
            font.pixelSize: 14
            font.bold: false
            anchors.centerIn: parent
            elide: Text.ElideRight
            textFormat: Text.PlainText
            text: modelData.text.replace('&#x27;', "'").replace('&#x22;', '"').replace('&lt;', "<").replace('&gt;', '>');

            color: ui.colors.white

            Component.onCompleted: {
                itemText.width = itemText.contentWidth < 264 ? itemText.contentWidth : 264
                rectDelegate.width = itemText.width + 32
            }
        }
    }

    Component {
        id: imageComponent

        DS3.Icon {
            id: itemImage

            anchors.centerIn: parent

            source: modelData.source
            color: modelData.color

            Component.onCompleted: {
                rectDelegate.width = itemImage.width + 32
            }
        }
    }

    Custom.HandMouseArea {
        id: mouseArea
    }
}