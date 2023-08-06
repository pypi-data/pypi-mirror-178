import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS" as DS


// Custom DS combobox
ComboBox {
    id: combobox

//  default text when current index is -1
    property var defaultText: tr.a911_not_chosen + "..."
//  number of visible items in combobox (property that defines the popup height: delegateHeight * visibleCount)
    property var visibleCount: 7
//  height of the delegate (preferably do not change)
    property var delegateHeight: 39
//  boolean value if something wrong (warning outline of content item based on this property)
    property bool error: false
//  delegate in the popup
    property Component delegateItem: DS.Text {
        anchors.verticalCenter: parent.verticalCenter

        text: delegateModelData
        size: 16

        color: combobox.currentIndex == delegateIndex ? ui.colors.interactive : ui.colors.base
    }

    height: 40

    model: []

    onActivated: error = false

    delegate: ItemDelegate {
        id: itemDelegate

        width: combobox.width
        height: delegateHeight

        Rectangle {
            id: delegateContent

            width: parent.width

            radius: (
                scrollBar.pressed
                || index == contentList.firstVisibleIndex
                || index == contentList.lastVisibleIndex
            ) ? 8 : 0

            anchors {
                top: index == contentList.firstVisibleIndex && contentList.hasHalfItem ? parent.verticalCenter : parent.top
                bottom: index == contentList.lastVisibleIndex && contentList.hasHalfItem ? parent.verticalCenter : parent.bottom
            }

            Rectangle {
                width: parent.width
                height: parent.height / 2

                anchors {
                    top: index == contentList.lastVisibleIndex ? parent.top : undefined
                    bottom: index == contentList.firstVisibleIndex ? parent.bottom : undefined
                }

                color: parent.color
                visible: parent.radius != 0 && !scrollBar.pressed
            }

            color: combobox.highlightedIndex == index && !scrollBar.pressed ? ui.backgrounds.high : ui.backgrounds.highest
        }

        Loader {
            width: parent.width - 16
            height: delegateHeight

            anchors.horizontalCenter: parent.horizontalCenter

            sourceComponent: delegateItem

            property var delegateModelData: modelData
            property var delegateIndex: index
        }

        DS.Image {
            width: 16
            height: 16

            anchors {
                right: parent.right
                rightMargin: 8
                verticalCenter: parent.verticalCenter
            }

            visible: combobox.currentIndex == index
            source: "qrc:/resources/images/Athena/common_icons/check.svg"
        }
    }

    indicator: Image {
        width: 24
        height: 24

        rotation: popup.visible ? 180 : 0

        anchors {
            right: combobox.right
            rightMargin: 8
            verticalCenter: combobox.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/arrowBottom.svg"
    }

    contentItem: DS.Text {
        leftPadding: 12
        rightPadding: 12

        text: combobox.displayText
        action: false
        size: 16

        Binding on text {
            when: countryPhoneCombo.currentIndex == -1 && !!defaultText
            value: defaultText
        }
    }

    background: Rectangle {
        color: ui.backgrounds.highest

        implicitWidth: 130
        implicitHeight: combobox.height
        border.width: combobox.popup.visible || combobox.error ? 1 : 0
        border.color: combobox.error ? ui.colors.attention : ui.colors.interactive
        radius: 8
    }

    popup: Popup {
        width: combobox.width
        height: Math.min(contentList.contentHeight, (delegateHeight + contentList.spacing) * visibleCount - contentList.spacing)
        padding: 0
        y: combobox.height + 8
        clip: true

        contentItem: ListView {
            id: contentList

            property var firstVisibleIndex: Math.floor(contentY / (delegateHeight + contentList.spacing))
            property var lastVisibleIndex: firstVisibleIndex + visibleCount - (hasHalfItem ? 0 : 1)
            property var hasHalfItem: contentY != (delegateHeight + contentList.spacing) * firstVisibleIndex

            anchors.fill: parent

            spacing: 1
            model: combobox.delegateModel
            interactive: false
            snapMode: scrollBar.pressed ? ListView.SnapOneItem : ListView.NoSnap

            ScrollBar.vertical: DS.ScrollBar {
                id: scrollBar

                stepSize: (delegateHeight + contentList.spacing) / (contentList.contentHeight - contentList.height)
                snapMode: ScrollBar.SnapAlways
            }

            MouseArea {
                id: contentListArea

                anchors.fill: parent

                z: 1

                onWheel: {
                    if (wheel.angleDelta.y > 0){
                        contentList.contentY = Math.max(
                            contentList.contentY - (delegateHeight + contentList.spacing) / 2,
                            0
                        )
                    }
                    else {
                        contentList.contentY = Math.min(
                            contentList.contentY + (delegateHeight + contentList.spacing) / 2,
                            contentList.contentHeight - contentList.height
                        )
                    }
                }
                onClicked: {
                    combobox.currentIndex = combobox.highlightedIndex
                    if (popup.opened) popup.close()
                    combobox.activated(combobox.currentIndex)
                }
            }
        }

        background: Rectangle {
            color: scrollBar.pressed ? ui.backgrounds.highest : ui.backgrounds.lowest
            radius: 10
        }
    }
}
