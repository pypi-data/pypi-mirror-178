import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS" as DS


Rectangle {
    id: userRegular

//  Photo of the user
    property alias image: image.source
//  User name
    property alias name: titleItem.text
//  User role
    property alias role: roleItemText.text
//  User email
    property alias email: emailItem.text

//  Gear icon clicked
    signal rightIconClicked

    onRightIconClicked: {
        console.log('settings entered')
    }

    implicitWidth: parent.width
    implicitHeight: 56

    color: ui.backgrounds.high

    Rectangle {
        id: defaultImage

        width: 40
        height: 40

        anchors.fill: image

        color: ui.backgrounds.low
        radius: width
        visible: image.status != Image.Ready

        DS.TextBodySRegular {
            anchors.centerIn: parent

            text: name.trim().split(/\s+/).splice(0, 2).reduce((value, token) => value + token.slice(0, 1), '')
            color: ui.colors.nonessential
        }
    }

    DS.Image {
        id: image

        width: 40
        height: 40

        anchors {
            left: parent.left
            leftMargin: 24
            verticalCenter: parent.verticalCenter
        }

        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
    }

    Rectangle {
        id: circle

        anchors.fill: image

        radius: width / 2
        visible: false
    }

    Column {
        anchors {
            left: image.right
            right: gear.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        Item {
            width: parent.width - 2 * parent.anchors.margins
            height: childrenRect.height

            DS.TextBodyMBold {
                id: titleItem

                width: parent.width

                elide: Text.ElideRight
            }

            Rectangle {
                id: roleItem

                width: childrenRect.width + 4
                height: childrenRect.height

                color: role == tr.user ? ui.colors.secondary : ui.colors.interactive
                radius: 2

                anchors {
                    left: parent.left
                    leftMargin: titleItem.contentWidth + 8
                    verticalCenter: titleItem.verticalCenter
                }

                DS.TextBodySRegular {
                    id: roleItemText

                    anchors.horizontalCenter: parent.horizontalCenter

                    color: ui.backgrounds.high
                }
            }
        }

        DS.TextBodySRegular {
            id: emailItem

            width: parent.width

            hasElide: true
            color: ui.colors.secondary
        }
    }

    DS.Icon {
        id: gear

        anchors {
            right: parent.right
            rightMargin: 24
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/qml/components/911/DS/assets/svg/Settings-M.svg"

        DS.MouseArea {
            onClicked: rightIconClicked()
        }
    }

    Rectangle {
        width: parent.width
        height: 1

        anchors.bottom: parent.bottom

        color: ui.backgrounds.lowest
    }
}
