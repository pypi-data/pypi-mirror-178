import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


ScrollView {
    id: tableScrollView

//  List of fractions that columns take. By default, all columns' fractions are equal
    property var fractions: []
//  List of columns' minimum widths. By default, each column has minimum width according to text width in header
    property var minimumWidths: []
//  Names of columns in header
    property var columnNames: []
//  Core of table. Main list with such attributes:
//  `model` - Model of table. Must be ListModel
//  `delegate` - Delegate for one table row
    property alias list: list
//  Width of the table content
    readonly property var tableContentWidth: list.headerItem.width
//  Default column widths. Calculated on completed automatically for column positioning
    readonly property var defaultColumnWidths: fractions.length
        ? fractions.map((f) => tableScrollView.width / totalFractions * f)
        : Array(columnNames.length).fill(tableScrollView.width / columnNames.length)
//  Total fractions, taken by columns. Can be changed by column widths resizing
    readonly property var totalFractions: fractions.reduce((a, w) => a+w)
//  Column width to use outside. For example, to create rowDelegate cells correctly
    readonly property var columnWidths: Array.from(list.headerItem.headerColumns).map((c) => c.width)

//  When table scrolled to bottom
    signal bottomReached()

    clip: true
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AlwaysOff

    Flickable {
        id: flickable

        contentWidth: list.width
        contentHeight: height
        boundsBehavior: Flickable.StopAtBounds

        ScrollBar.horizontal: ScrollBar {
            padding: 0
            minimumSize: 0.1
            visible: parent.width < parent.contentWidth

            anchors {
                left: parent.left
                bottom: parent.bottom
                right: parent.right
            }

            contentItem: Item {
                implicitWidth: 100
                implicitHeight: indicator.height + 8

                Rectangle {
                    id: indicator

                    width: parent.width
                    height: tableViewHorizontalScrollbarArea.containsMouse ? 8 : 4

                    anchors {
                        left: parent.left
                        bottom: parent.bottom
                        right: parent.right
                        margins: 8
                    }

                    radius: width / 2
                    color: ui.ds3.figure.secondary

                    Behavior on height {
                        NumberAnimation {
                            duration: 100
                        }
                    }
                }
            }

            DS3.MouseArea {
                id: tableViewHorizontalScrollbarArea

                cursorShape: Qt.ArrowCursor

                onPressed: mouse.accepted = false
            }
        }

        ListView {
            id: list

            width: headerItem.width
            height: parent.height

            spacing: 1
            headerPositioning: ListView.OverlayHeader
            boundsBehavior: Flickable.StopAtBounds
            interactive: false

            ScrollBar.vertical: DS3.ScrollBar {
                id: listViewScrollBar

                anchors.topMargin: list.headerItem.height

                hasPadding: true
                parent: list.parent.parent
                visible: tableScrollView.height < list.contentHeight
            }

            header: Rectangle {
                property alias headerColumns: headerColumns.children

                // Calculating total width from all columns widths
                width: tableScrollView.columnWidths.reduce((a,w)=>a+w)
                height: 32

                z: 2
                color: ui.ds3.bg.high

                Row {
                    id: headerColumns

                    height: parent.height

                    spacing: 0
                    clip: true

                    Repeater {
                        id: tableHeaderItem

                        model: tableScrollView.columnNames

                        delegate: Item {
                            id: headerDelegate

                            width: div.x + div.width
                            height: parent.height

                            DS3.Text {
                                // Fake component with same text to determine it's content width
                                id: fakeText

                                text: modelData
                                visible: false
                                style: headerColumnItem.style
                            }

                            DS3.Text {
                                id: headerColumnItem

                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    left: parent.left
                                    leftMargin: index == 0 ? 16 : 8
                                    right: parent.right
                                    rightMargin: 8
                                }

                                text: modelData
                                color: ui.ds3.figure.secondary

                                Component.onCompleted: {
                                    area.drag.minimumX = !minimumWidths.length
                                        ? fakeText.contentWidth + anchors.leftMargin + div.width
                                        : minimumWidths[index]
                                    hasElide = true
                                }
                            }

                            Item {
                                id: div

                                width: visible ? 8 : 0
                                height: parent.height

                                x: Math.max(
                                    (index == tableHeaderItem.count - 1
                                        ? Math.max(tableScrollView.width - headerDelegate.x, tableScrollView.defaultColumnWidths[index])
                                        : tableScrollView.defaultColumnWidths[index]) - width,
                                    area.drag.minimumX
                                )
                                visible: index != tableHeaderItem.count - 1

                                Rectangle {
                                    width: 2
                                    height: parent.height - 8

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        right: parent.right
                                    }

                                    radius: 1
                                    color: ui.ds3.bg.highest
                                }

                                DS3.MouseArea {
                                    id: area

                                    cursorShape: Qt.SizeHorCursor
                                    drag {
                                        target: parent
                                        axis: Drag.XAxis
                                        maximumX: tableScrollView.width - width
                                    }

                                    onReleased: {
                                        fractions[index] = headerDelegate.width / defaultColumnWidths[index] * fractions[index]
                                    }
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 1

                    anchors.bottom: parent.bottom

                    color: ui.ds3.bg.lowest
                }
            }

            MouseArea {
                readonly property real velocity: 1

                anchors.fill: parent

                acceptedButtons: Qt.NoButton
                z: -1

                onWheel: (e) => {
                    let movementY = -(e.angleDelta.y / velocity)
                    let movementX = -(e.angleDelta.x / velocity)

                    if (e.modifiers & Qt.ShiftModifier) {
                        movementX = movementY
                        movementY = 0
                    }

                    if (movementY && listViewScrollBar.visible && flickBlock.flickingDirection != 1) {
                        flickBlock.flickingDirection = 2
                        if (list.contentY + list.headerItem.height + movementY + list.height > list.contentHeight) {
                            list.contentY = list.contentHeight - list.height - list.headerItem.height
                        } else if (list.contentY + list.headerItem.height + movementY < 0) {
                            list.contentY = - list.headerItem.height
                        } else {
                            list.contentY += movementY
                        }
                    } else if (movementX && flickable.ScrollBar.horizontal.visible && flickBlock.flickingDirection != 2) {
                        flickBlock.flickingDirection = 1
                        flickable.contentX = Math.max(
                            Math.min(flickable.contentX + movementX, flickable.contentWidth - flickable.width),
                            0
                        )
                    }
                }

                Timer {
                    id: flickBlock

                    // 0 - not flicking, 1 - x axis, 2 - y axis
                    property int flickingDirection: 0

                    interval: 100
                    onFlickingDirectionChanged: if (flickingDirection) restart()
                    onTriggered: flickingDirection = 0
                }
            }

            onContentYChanged: {
                if (contentY == contentHeight - height - headerItem.height) {
                    bottomReached()
                }
            }
        }
    }
}
