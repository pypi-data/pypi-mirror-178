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
//  When you need to change the sort order
    property bool isReversedSorting: false
//  Which page is chosen
    property var currentPage: ""

    signal headerChoosen(int headerIndex, int headerSubIndex)

    clip: true
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AlwaysOff

    Flickable {
        id: flickable

        contentWidth: list.width
        contentHeight: height
        boundsBehavior: Flickable.StopAtBounds

        ScrollBar.horizontal: ScrollBar {
            anchors {
                left: parent.left
                bottom: parent.bottom
                right: parent.right
            }

            padding: 0
            minimumSize: 0.1
            visible: parent.width < parent.contentWidth

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

            property var checkedCounter: 0
            property var allChecked: count == checkedCounter

            width: headerItem.width
            height: parent.height
            cacheBuffer: 1000

            spacing: 1
            headerPositioning: ListView.OverlayHeader
            boundsBehavior: Flickable.StopAtBounds
            interactive: false

            function selectAllLocally() {
                for(let child = 0; child < list.count; child++) {
                    let reportItem = list.itemAtIndex(child)

                    if (reportItem.objectName == "objectsArchiveInfoDelegate") {
                        reportItem.checked = !allChecked
                        objectArchiveSelectedReports.push(reportItem.reportId)
                        objectArchiveSelectedReportsChanged()
                    }
                }
                checkedCounter = allChecked ? 0 : count
                if (checkedCounter == 0) {
                    objectArchiveSelectedReports = []
                }
            }

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
                height: 48

                z: 2
                color: ui.ds3.bg.high

                Row {
                    id: headerColumns

                    height: parent.height

                    spacing: 0
                    clip: true

                    Repeater {
                        id: tableHeaderItem

                        property int currentIndex: 0

                        model: tableScrollView.columnNames

                        delegate: Item {
                            id: headerDelegate

                            width: tableScrollView.defaultColumnWidths[index]
                            height: 56

                            DS3.ResetAll {
                                id: resetAllButton

                                visible: index == 0
                                size: DS3.ResetAll.ComponentSize.S

                                clickedArea.onClicked: {
                                    checked = !checked
                                    if (currentPage === "Objects") {
                                        if (checked) {
                                            context.getAllHubsIds(searchFieldObjects)
                                           }
                                        else if (!checked) {
                                            context.clearAllItemsIds("hub_hex_id")
                                        }
                                    }
                                    else if (currentPage === "Archive") {
                                        if (checked) {
                                            context.getAllReportsIds(searchFieldArchive)
                                        }
                                        else if (!checked) {
                                            context.clearAllItemsIds("report_id")
                                        }
                                    }
                                    else if (currentPage === "Objects Archive") {
                                        list.selectAllLocally()
                                    }
                                }

                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    left: parent.left
                                    leftMargin: 16
                                }
                            }

                            DS3.TableHeaderXS {
                                property bool isLastDelegate: index == tableHeaderItem.count - 1

                                anchors {
                                    left: index == 0 ? resetAllButton.right : (isLastDelegate ? undefined : parent.left)
                                    leftMargin: 8
                                    right: isLastDelegate ? parent.right : undefined
                                    rightMargin: 24
                                    verticalCenter: parent.verticalCenter
                                }

                                sheetActionListView.model: {
                                    if (modelData == tr.a911_object) return [tr.filter_by_object_name, tr.filter_by_address]
                                    if (modelData == tr.report_requested_by) return [tr.filter_by_name, tr.filter_by_email]
                                    return []
                                }
                                titleItem.text: modelData
                                buttonIcon {
                                    visible: tableHeaderItem.currentIndex == index
                                    color: ui.ds3.figure.secondary
                                }
                                isReversed: isReversedSorting
                                onChoosen: {
                                    tableHeaderItem.currentIndex = index
                                    headerChoosen(index, selectedIndex, isReversed)
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

            Rectangle {
                id: emptySearch

                anchors.centerIn: parent

                visible: {
                    if (currentPage === "Objects") return !context.hubsNumber
                    if (currentPage === "Archive") return !context.allArchivesInfoView.length
                    return false
                }

                DS3.Image {
                    id: logoImage

                    width: 160
                    height: 160

                    anchors.centerIn: parent

                    source: "qrc:/resources/images/Athena/common_icons/AjaxLogo.svg"
                }

                DS3.Text {
                    anchors{
                        top: logoImage.bottom
                        horizontalCenter: parent.horizontalCenter
                    }

                    text: tr.nothing_found_in_search
                    style: ui.ds3.text.body.MRegular
                    color: ui.ds3.figure.nonessential
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
