import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/parts/headers" as Headers
import "qrc:/resources/qml/screens/home/pages/objects/parts/delegates" as Delegates


Item {
    id: categoriesList
    anchors.fill: parent

    property alias objectsTable: objectsTable

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
    }

    Connections {
        target: objectsSidebar

        onReloadModel: {
            objectsTable.positionViewAtBeginning()
        }
    }

    ScrollView {
        id: scrollView
        clip: true
        width: parent.width
        anchors {
            top: parent.top
            bottom: trashFooter.top
        }

        ScrollBar.horizontal.policy: {
            if (objectsTable.width > scrollView.width) {
                return ScrollBar.AlwaysOn
            }
            return ScrollBar.AlwaysOff
        }

        Flickable {
            contentWidth: objectsTable.width
            contentHeight: categoriesList.height - trashFooter.height

            ListView {
                id: objectsTable
                clip: true
                spacing: 0
                width: headerItem.width
                height: parent.height
                headerPositioning: ListView.OverlayHeader
                boundsBehavior: Flickable.StopAtBounds

                model: appCompany.filtered_objects_model

                property var action: null

                Custom.EmptySpaceLogo {
                    visible: objectsTable.model.length == 0
                }

                Connections {
                    target: app.incident_module

                    onGetActivitiesSuccess: {
                        if (objectsTable.action) objectsTable.action(activities)
                    }
                }

                property var mode: objectsSidebar.currentTab.mode

                header: {
                    if (mode == "active") return activeHeader
                    if (mode == "with_installation_services") return withInstallationServicesHeader
                    if (mode == "armed") return armedHeader
                    if (mode == "disarmed") return disarmedHeader
                    if (mode == "sleep") return sleepHeader

                    if (mode == "offline") return offlineHeader
                    if (mode == "warnings") return warningsHeader
                    if (mode == "no_agreement") return noAgreementHeader

                    if (mode == "installers") return installersHeader
                    if (mode == "connect") return connectHeader
                    if (mode == "disconnect") return disconnectHeader
                    if (mode == "trash") return trashHeader

                    return nullComp
                }

                delegate: {
                    if (mode == "active") return activeDelegate
                    if (mode == "with_installation_services") return withInstallationServicesDelegate
                    if (mode == "armed") return armedDelegate
                    if (mode == "disarmed") return disarmedDelegate
                    if (mode == "sleep") return sleepDelegate

                    if (mode == "offline") return offlineDelegate
                    if (mode == "warnings") return warningsDelegate
                    if (mode == "no_agreement") return noAgreementDelegate

                    if (mode == "installers") return installersDelegate
                    if (mode == "connect") return connectDelegate
                    if (mode == "disconnect") return disconnectDelegate
                    if (mode == "trash") return trashDelegate

                    return nullComp
                }

                ScrollBar.vertical: Custom.ScrollBar {
                    id: control
                    parent: scrollView
                    anchors {
                        top: parent.top
                        topMargin: 32
                        right: parent.right
                        bottom: parent.bottom
                    }

                    policy: {
                        if (objectsTable.contentHeight > objectsTable.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }

                    property var lastPosition: 0.0
                    property var direction: 0   // 0 - up, 1 - down
                    property var prevAB: 0

                    onPositionChanged: {
                        if (control.position - lastPosition > 0) {
                            direction = 1
                        } else {
                            direction = 0
                        }
                        lastPosition = control.position

                        var a = 1 - (control.position + control.size)
                        var b = 1 - (control.position + control.size/2)

                        if (a/b < 0.4 && direction == 1) {
                            if (prevAB >= 0.4) {
                                app.facility_module.get_category(objectsSidebar.currentTab.mode, false)
                            }
                            if (control.pressed && lastPosition) {
                                control.position = lastPosition
                            }
                        }

                        control.prevAB = a/b
                    }
                }
            }
        }
    }

    TrashFooter {
        id: trashFooter
        width: parent.width
        anchors {
            bottom: parent.bottom
        }
    }

    Custom.BlockLoading {
        minTime: 300
        startSignals: [objectsSidebar.reloadModel, app.facility_module.getCategory]
        stopSignals: [app.facility_module.findFacilitySuccess, app.facility_module.getCategoryFailed]
    }

    Component {
        id: nullComp
        Item {}
    }


    //  headers

    Component {
        id: activeHeader
        Headers.Active {}
    }

    Component {
        id: withInstallationServicesHeader
        Headers.WithInstallationServices {}
    }

    Component {
        id: armedHeader
        Headers.Armed {}
    }

    Component {
        id: disarmedHeader
        Headers.Disarmed {}
    }

    Component {
        id: sleepHeader
        Headers.Sleep {}
    }

    Component {
        id: offlineHeader
        Headers.Offline {}
    }

    Component {
        id: warningsHeader
        Headers.Warnings {}
    }

    Component {
        id: noAgreementHeader
        Headers.NoAgreement {}
    }

    Component {
        id: installersHeader
        Headers.Installers {}
    }

    Component {
        id: connectHeader
        Headers.Connect {}
    }

    Component {
        id: disconnectHeader
        Headers.Disconnect {}
    }

    Component {
        id: trashHeader
        Headers.Trash {}
    }


    //  delegates

    Component {
        id: activeDelegate
        Delegates.Active {}
    }

    Component {
        id: withInstallationServicesDelegate
        Delegates.WithInstallationServices {}
    }

    Component {
        id: armedDelegate
        Delegates.Armed {}
    }

    Component {
        id: disarmedDelegate
        Delegates.Disarmed {}
    }

    Component {
        id: sleepDelegate
        Delegates.Sleep {}
    }

    Component {
        id: offlineDelegate
        Delegates.Offline {}
    }

    Component {
        id: warningsDelegate
        Delegates.Warnings {}
    }

    Component {
        id: noAgreementDelegate
        Delegates.NoAgreement {}
    }

    Component {
        id: installersDelegate
        Delegates.Installers {}
    }

    Component {
        id: connectDelegate
        Delegates.Connect {}
    }

    Component {
        id: disconnectDelegate
        Delegates.Disconnect {}
    }

    Component {
        id: trashDelegate
        Delegates.Trash {}
    }
}