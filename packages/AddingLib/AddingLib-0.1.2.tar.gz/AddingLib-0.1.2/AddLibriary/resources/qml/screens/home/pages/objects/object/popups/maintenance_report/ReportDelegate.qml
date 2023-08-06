import QtQuick 2.12
import QtQuick.Dialogs 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: archiveDelegateWrapper

//  Determine if mouse pointer is on a row
    property bool isSelected: listView.currentIndex === index
//  Select color of row
    property var rowColor: isSelected ? ui.ds3.bg.high : ui.ds3.bg.highest
//  Alias for check combobox
    property alias checked: archiveObjectInfoDelegate.checked
//  Report id
    property var reportId: modelData.report_id

    function selectDelegate() {
        archiveObjectInfoDelegate.checked = !archiveObjectInfoDelegate.checked
        if (archiveObjectInfoDelegate.checked) {
            objectArchiveSelectedReports.push(modelData.report_id)
        } else {
            objectArchiveSelectedReports = objectArchiveSelectedReports.filter(selectedReport => selectedReport !== modelData.report_id)
        }
        objectArchiveSelectedReportsChanged()
    }

    width: parent.width
    height: 56

    objectName: "objectsArchiveInfoDelegate"

    DS3.MouseArea {
        onPositionChanged: listView.currentIndex = index
        onClicked: selectDelegate()
        onExited: listView.currentIndex = -1
    }

    Row {
        id: archiveObjectInfoDelegate

        height: 56

        //  Whether hub is selected for report generating
        property alias checked: selectArchive.checked

        Rectangle {
            height: parent.height
            width: objectArchiveList.columnWidths[0]

            anchors.rightMargin: 8

            color: rowColor

            Row {
                anchors.verticalCenter: parent.verticalCenter

                DS3.Spacing {
                    width: 16
                }

                DS3.Select {
                    id: selectArchive

                    size: DS3.Select.ComponentSize.S

                    clickedArea.onClicked: {
                        selectDelegate()
                    }
                }

                DS3.Spacing {
                    width: 16
                }

                DS3.Text {
                    text: modelData.sequence_number
                }
            }
        }

        Rectangle {
            width: objectArchiveList.columnWidths[1]
            height: parent.height

            color: rowColor

            Column {
                anchors.verticalCenter: parent.verticalCenter

                leftPadding: 16

                DS3.Text {
                    text: modelData.user_full_name
                }

                DS3.Text {
                    text: modelData.user_email
                    style: ui.ds3.text.body.SRegular
                    color: ui.ds3.figure.secondary
                }
            }
        }

        Rectangle {
            id: date

            width: objectArchiveList.columnWidths[2]
            height: parent.height

            color: rowColor

            DS3.MouseArea {
                onPositionChanged: listView.currentIndex = index
            }

            DS3.ButtonTextRect {
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    right: parent.right
                }

                buttonIconSource: "qrc:/resources/images/Athena/common_icons/Download-S.svg"
                text: tr.new_version_download
                visible: isSelected
                onClicked: {
                    reportIdToSave = modelData.report_id
                    saveFileDialog.open()
                }
            }

            DS3.Text {
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    rightMargin: 16
                    right: parent.right
                }

                text: modelData.report_date
                horizontalAlignment: Text.AlignRight
                visible: !isSelected
            }
        }
    }
}
