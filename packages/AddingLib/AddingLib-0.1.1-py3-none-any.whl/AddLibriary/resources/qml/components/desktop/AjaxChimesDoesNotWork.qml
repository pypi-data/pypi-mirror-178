import QtQuick 2.13
import QtQuick.Controls 2.12


Rectangle {
    width: 360
    height: 700

    anchors.left: parent.left

    color: ui.colors.dark3

    AjaxPopupCloseHeader {
        id: closeItem

        width: parent.width
        height: 48

        anchors {
            top: parent.top
        }

        label: tr.chime_activation
    }

    Column {
        width: parent.width - 64

        anchors.centerIn: parent

        spacing: 16

        Item {
            width: chimesWorkPartiallyImage.width
            height: chimesWorkPartiallyImage.height + 8

            anchors.horizontalCenter: parent.horizontalCenter

            Image {
                id: chimesWorkPartiallyImage

                width: 136
                height: 136

                source: "qrc:/resources/images/desktop/chimes/GroupsChimesWorkPartially.svg"
            }
        }

        Text {
            id: chimesDoesNotWorkTitle

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.chimes_does_not_work_title
            horizontalAlignment: Text.AlignHCenter
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 16
            font.weight: Font.Bold
            wrapMode: Text.WordWrap
        }

        Text {
            id: chimesWorkPartiallyInfo

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.chimes_does_not_work_info
            horizontalAlignment: Text.AlignHCenter
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 16
            wrapMode: Text.WordWrap
        }
    }
}
