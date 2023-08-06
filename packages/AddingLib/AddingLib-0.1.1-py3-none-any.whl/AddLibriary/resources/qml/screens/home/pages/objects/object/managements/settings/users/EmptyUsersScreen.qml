import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


Column {
    width: parent.width

    spacing: 16

    DS3.PlugImage {
        anchors.horizontalCenter: parent.horizontalCenter

        source: "qrc:/resources/images/Athena/common_icons/Users-XL.svg"
    }

    Item {
        id: textItem

        width: parent.width
        height: 8 + addText.height

        DS3.Text {
            id: addText

            width: parent.width - 48
            height: contentHeight

            text: tr.add_first_user_general
            style: ui.ds3.text.body.LRegular
            color: ui.ds3.figure.secondary
            horizontalAlignment: Text.AlignHCenter

            anchors {
                horizontalCenter: parent.horizontalCenter
                top: parent.top
                topMargin: 8
            }
        }
    }
}