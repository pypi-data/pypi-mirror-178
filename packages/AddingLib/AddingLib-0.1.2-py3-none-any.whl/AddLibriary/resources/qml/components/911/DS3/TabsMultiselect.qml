import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  Example of item: {icon: "path", checked: true, enabled: true}
    property var tabs: []

    width: row.width
    height: 40

    color: ui.ds3.figure.transparent
    border {
        width: 1
        color: ui.ds3.figure.disabled
    }
    radius: 8

    Row {
        id: row

        height: parent.height

        Repeater {
            id: tabsModel

            model: tabs

            Item {
                id: delegate

                property var checked: modelData.checked

                width: 54
                height: parent.height

                enabled: modelData.enabled

                Rectangle {
                    anchors.fill: parent

                    color: delegate.checked ? ui.ds3.figure.interactive : ui.ds3.figure.transparent
                    layer.enabled: true
                    layer.effect: OpacityMask {
                        maskSource: Item {
                            width: delegate.width
                            height: delegate.height

                            Rectangle {
                                anchors {
                                    fill: parent
                                    rightMargin: index == tabsModel.count - 1 ? 0 : -8
                                    leftMargin: index == 0 ? 0 : -8
                                }

                                radius: 8
                            }
                        }
                    }
                }

                DS3.Icon {
                    anchors.centerIn: parent

                    source: modelData.icon
                    opacity: enabled ? 1 : 0.3
                    color: delegate.checked ? ui.ds3.figure.inverted : ui.ds3.figure.interactive
                }

                Rectangle {
                    width: 1
                    height: parent.height

                    anchors.right: parent.right

                    visible: index < tabsModel.count - 1
                    color: ui.ds3.figure.disabled
                }

                DS3.MouseArea {
                    onClicked: {
                        tabs[index].checked = !checked
                        tabsChanged()
                    }
                }
            }
        }
    }
}
