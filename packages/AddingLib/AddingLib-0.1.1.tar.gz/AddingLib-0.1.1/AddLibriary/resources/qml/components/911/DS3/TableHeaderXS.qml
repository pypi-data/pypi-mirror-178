import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: tableHeaderXS

//  Use this property to set title
    property alias titleItem: titleItem
//  Use this to change buttonIcon
    property alias buttonIcon: buttonIcon
//  Use this to change sheetAction ListView
    property alias sheetActionListView: sheetActionListView
//  Need show sheet action
    readonly property bool isSheetActionVisible: !!sheetActionListView.model.length
//  True when this header is selected for sorting
    property bool isSelected: false
//  Show sort order
    property bool isReversed: false
//  Show current index in sheet action list view
    property int selectedListViewIndex: -1
//  True when header need to be clickable
    property bool isHovered: true
//  When the component should be centered
    property bool isCenter: true

    signal choosen(int selectedIndex)

    width: mainRow.width + 16
    height: 32

    color: mouseArea.containsMouse ? ui.ds3.bg.base : ui.ds3.bg.high
    radius: 12

    Row {
        id: mainRow

        height: 16

        anchors.centerIn: isCenter ? parent : undefined

        spacing: 8

        DS3.Text {
            id: titleItem

            anchors.verticalCenter: parent.verticalCenter

            style: ui.ds3.text.body.SRegular
            color: mouseArea.containsMouse ? ui.ds3.figure.nonessential : ui.ds3.figure.secondary
        }

        DS3.Icon {
            id: buttonIcon

            anchors.verticalCenter: parent.verticalCenter

            color: mouseArea.containsMouse ? ui.ds3.figure.nonessential : ui.ds3.figure.secondary
            source: isReversed ?
                "qrc:/resources/images/Athena/common_icons/VerticalArrow-Down-S.svg" :
                "qrc:/resources/images/Athena/common_icons/VerticalArrow-S.svg"
            visible: isSelected
        }
    }

    DS3.MouseArea {
        id: mouseArea

        interval: 0

        visible: isHovered

        onEntered: {
            sheetAction.open()
            closeTimer.stop()
        }
        onExited: closeTimer.start()

        onClicked: {
            if (!isSheetActionVisible) choosen(-1)
            selectedListViewIndex = -1
        }
    }

    DS3.SheetAction {
        id: sheetAction

        width: 180

        parent: tableHeaderXS
        y: parent.height

        ListView {
            id: sheetActionListView

            width: parent.width
            height: contentHeight

            model: []
            delegate: DS3.SettingsSort {
                color: delegateMouseArea.containsMouse ? ui.ds3.bg.high : ui.ds3.bg.highest
                titleItem.text: modelData
                iconItem {
                    source: isReversed ?
                        "qrc:/resources/images/Athena/common_icons/VerticalArrow-Down-S.svg" :
                        "qrc:/resources/images/Athena/common_icons/VerticalArrow-S.svg"
                    color: ui.ds3.figure.interactive
                    visible: selectedListViewIndex == index
                }
                DS3.MouseArea {
                    id: delegateMouseArea

                    onEntered: closeTimer.stop()
                    onExited: closeTimer.start()

                    onClicked: {
                        choosen(index)
                        selectedListViewIndex = index
                    }
                }
            }

            Timer {
                id: closeTimer

                interval: 300

                onTriggered: {
                    sheetAction.close()
                }
            }
        }
    }
}