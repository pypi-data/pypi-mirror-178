import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsContainer {
//  If accordion is opened
    property bool collapsed: false
//  Title of the item
    property alias title: atomTitle.title
//  Subtitle of the item
    property alias subtitle: atomTitle.subtitle
//  Model for listView
    property var repeaterModel: []
//  Image in left side
    property alias hasIcon: leftIcon.visible
//  Source of the image
    property alias imageSource: leftIcon.source
    width: 452

    Rectangle {
        id: mainRectangle

        width: parent.width
        height: 68

        color: ui.ds3.bg.highest

        DS3.Icon {
            id: leftIcon

            anchors {
                left: parent.left
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }

            visible: false
        }

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: hasIcon ? 56 : 16
            }

            subtitle: repeaterModel.length
            isPrimary: false
            subtitleItem.hasElide: true
        }

        DS3.Icon {
            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            source: collapsed ? "qrc:/resources/images/Athena/common_icons/Cross-S.svg" : "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
        }

        DS3.MouseArea {
            onClicked: {
                collapsed = !collapsed
            }
        }
    }

    Item {
        width: parent.width
        height: listView.height

        visible: collapsed

        ListView {
            id: listView

            width: parent.width
            height: contentHeight

            model: repeaterModel
            spacing: 1

            delegate: DS3.InfoTitle {
                width: parent.width
                height: 48

                atomTitle.title: repeaterModel[index]
            }
        }
    }
}