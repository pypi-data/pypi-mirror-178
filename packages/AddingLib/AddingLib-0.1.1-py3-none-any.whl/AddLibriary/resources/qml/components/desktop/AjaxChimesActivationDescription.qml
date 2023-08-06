import QtQuick 2.13
import QtQuick.Controls 2.12


Item {
    property bool halfWork: management && management.groups.chimes_half_ready_groups_exist

    width: parent.width
    height: childrenRect.height + 48

    Column {
        width: parent.width

        spacing: 16

        Item {
            width: parent.width
            height: 160

            Image {
                id: chimesWorkPartiallyImage

                width: 136
                height: 136

                anchors {
                    horizontalCenter: parent.horizontalCenter
                    bottom: parent.bottom
                }

                source: halfWork
                    ? "qrc:/resources/images/desktop/chimes/GroupsChimesWorkPartially.svg"
                    : "qrc:/resources/images/desktop/chimes/GroupsChimesWork.svg"
            }
        }

        Text {
            id: chimesWorkPartiallyTitle

            anchors.horizontalCenter: parent.horizontalCenter

            visible: halfWork
            text: tr.chimes_work_partially_title
            horizontalAlignment: Text.AlignHCenter
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 16
            font.weight: Font.Bold
            width: parent.width - 64
            wrapMode: Text.WordWrap
        }

        Text {
            id: chimesWorkPartiallyInfo

            anchors.horizontalCenter: parent.horizontalCenter

            text: halfWork ? tr.chimes_work_partially_info : tr.turn_on_chimes_in_group_mode_info
            horizontalAlignment: Text.AlignHCenter
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 16
            width: parent.width - 64
            wrapMode: Text.WordWrap
        }
    }
}
