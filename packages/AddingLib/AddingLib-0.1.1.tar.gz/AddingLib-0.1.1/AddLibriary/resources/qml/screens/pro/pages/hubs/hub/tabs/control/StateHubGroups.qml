import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: itemGroups
    anchors.fill: parent

    GridView {
        id: gridView
        model: management.filtered_groups
        clip: true

        anchors.centerIn: parent
        width: {
            if (gridView.count <= 4 ) {
                return gridView.cellWidth * gridView.count
            }
            return gridView.cellWidth * 4
        }

        height: {
            var heightGrid = Math.ceil(gridView.count / 4) * gridView.cellHeight
            return heightGrid > parent.height ? parent.height : heightGrid
        }

        cellWidth: 160
        cellHeight: 160
        delegate: Rectangle {
            width: gridView.cellWidth
            height: gridView.cellHeight
            radius: 10
            color: mouse.containsMouse ? ui.colors.dark2 : "transparent"
            Custom.UserImage {
                Rectangle {
                    visible: group.state === "ARMED"
                    anchors.fill: parent
                    color: ui.colors.green1
                    opacity: 0.4
                    radius: height / 2
                }
                id: groupImg
                width: 80
                height: 80
                anchors.centerIn: parent
                imageSource: group.small_image_link === "WRONG" ? "" : group.small_image_link
                userName: group.name
                Rectangle {
                    width: 32
                    height: 32
                    color: ui.colors.dark3
                    radius: height / 2
                    anchors {
                        left: parent.left
                        leftMargin: -5
                        bottom: parent.bottom
                    }
                    Image {
                        width: 17
                        height: 18
                        source: group.state === "ARMED" ? "qrc:/resources/images/pro/icons_groups/armed.svg" : "qrc:/resources/images/pro/icons_groups/disarmed.svg"
                        anchors.centerIn: parent
                    }
                }
            }
            Custom.HandMouseArea {
                id: mouse
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    gridView.currentIndex = index
                    app.hub_management_module.perform_group_security_action(group, false)
                }
            }
            Custom.FontText {
                width: 80
                text: group.name
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                textFormat: Text.AutoText
                color: ui.colors.light4
                anchors {
                    top: groupImg.bottom
                    topMargin: 10
                    horizontalCenter: groupImg.horizontalCenter
                }
            }
        }
    }
}