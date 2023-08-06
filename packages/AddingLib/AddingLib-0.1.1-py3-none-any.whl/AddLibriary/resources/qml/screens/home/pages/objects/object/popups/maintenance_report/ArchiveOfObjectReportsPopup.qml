import QtQuick 2.12
import QtQuick.Dialogs 1.3

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/app/modules/views/maintenance_report/popups" as MRPopups


DS3.Popup {
    id: reportsObjectArchivePopup

//  Property for global user settings, because FileDialog has own settings property
    property var appSettings: settings
    property var objectArchiveSelectedReports: []
    property string reportIdToSave: ""
    property alias listView: objectArchiveList.list

    Component.onCompleted: {
        app.maintenanceReport.getObjectArchivesInfo(facility.hub_id)
        app.maintenanceReport.startDownloadingStream()
    }

    Component.onDestruction: {
        app.maintenanceReport.cancelDownloadingStream()
    }

    width: 800
    height: 540

    sideMargins: 0
    backgroundColor: ui.ds3.bg.base

    MRPopups.DownloadStackPopup {
        popupContext: app.maintenanceReport
    }

    FileDialog {
        id: saveFileDialog

        selectFolder: true
        folder: appSettings.file_path ? appSettings.file_path : shortcuts.home
        title: tr.select_folder_desktop

        onRejected: saveFileDialog.close()

        onAccepted: {
            saveFileDialog.close()
            appSettings.file_path = fileUrl
            if (reportIdToSave) {
                app.maintenanceReport.downloadReports([reportIdToSave], fileUrl)
                reportIdToSave = ""
            } else {
                app.maintenanceReport.downloadReports(objectArchiveSelectedReports, fileUrl)
            }
        }
    }

    header: DS3.NavBarModal {
        headerText: tr.archive_of_reports_title
        onClosed: () => {
            reportsObjectArchivePopup.close()
        }
        backgroundColor: ui.ds3.bg.high
        isNavigationTextLeft: true
        navigationText: tr.create_report_button

        onNavigationTextClicked: {
            objectsStack.hubHexId = facility.hub_id
            objectsStack.objectsScreenLoaderSource = "qrc:/resources/qml/screens/home/pages/objects/maintenance_report/MaintenanceReport.qml"
        }
    }

    DS3.Spacing {
        height: 1
    }

    Rectangle {
        width: parent.width
        height: 56

        color: ui.ds3.bg.high

        DS3.Text {
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
                leftMargin: 12
            }

            text: tr.five_last_reports_descr
            color: ui.ds3.figure.nonessential
            style: ui.ds3.text.body.MRegular
        }

        DS3.ButtonTextRect {
            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            visible: objectArchiveSelectedReports.length > 0
            text: tr.download_selected_button
            buttonIconSource: "qrc:/resources/images/Athena/common_icons/Download-S.svg"

            onClicked: saveFileDialog.open()
        }
    }

    DS3.ReportTableView {
        id: objectArchiveList

        width: parent.width
        height: 400

        columnNames: [tr.report_id, tr.report_requested_by, tr.date_of_report]
        fractions: [0.6,1,0.4]
        currentPage: "Objects Archive"

        list {
            model: app.maintenanceReport.sortedAllObjectArchivesInfo
            delegate: ReportDelegate {}
            currentIndex: -1
        }
        isReversedSorting: app.maintenanceReport.isObjectArchiveSortingReversed
        onHeaderChoosen: {
            const sortingFieldMapper = [
                "report_id",
                ["user_full_name", "user_email"],
                "report_date"
            ]
            var fieldForSorting = headerSubIndex >= 0 ?
                sortingFieldMapper[headerIndex][headerSubIndex] :
                sortingFieldMapper[headerIndex]
            if (app.maintenanceReport.objectArchiveSorter == fieldForSorting) {
                app.maintenanceReport.isObjectArchiveSortingReversed = !app.maintenanceReport.isObjectArchiveSortingReversed
            } else {
                app.maintenanceReport.objectArchiveSorter = fieldForSorting
            }
        }
    }
}