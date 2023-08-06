import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/parts/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: objectsSidebar

    color: ui.colors.dark3

    signal reloadModel()
    signal blockElement()

    onReloadModel: {
        app.facility_module.get_categories_counters(objectsSidebar.enabledCategories)
        if (!!currentTab) app.facility_module.get_category(objectsSidebar.currentTab.mode, true)
    }

    /*
        Depends on Active-Tab visibility.
    */
    property var rights: appUser.employee_roles_access_rights
    property var mrRights: {
        let access = []

        appUser.role.forEach((role) => {
            access.push(rights[role].includes("MAINTENANCE_REPORT_MAKE"))
        })

        if (access.some(item => item)) {
            return true
        }
        return false
    }
    property var currentTab: (
        companyAccess.OBJECTS_ACTIVE && activeTab
        || companyAccess.OBJECTS_WITH_INSTALLATION_SERVICE && allInstallationObjectsTab
        || null
    )

    readonly property var enabledCategories: ({
        active: companyAccess.OBJECTS_ACTIVE,
        armed: companyAccess.OBJECTS_ARMED,
        disarmed: companyAccess.OBJECTS_DISARMED,
        sleep: companyAccess.OBJECTS_SLEEPING,
        offline: companyAccess.OBJECTS_OFFLINE,
        warnings: companyAccess.OBJECTS_MALFUNCTIONS,
        no_agreement: companyAccess.OBJECTS_WITHOUT_CONTRACT,
        with_installation_services: companyAccess.OBJECTS_WITH_INSTALLATION_SERVICE,
        installers: companyAccess.OBJECTS_MONITORING_REQUEST_FROM_INSTALLER,
        connect: companyAccess.OBJECTS_MONITORING_REQUEST_FROM_USER,
        disconnect: companyAccess.OBJECTS_WITHDRAWN_FROM_MONITORING,
        trash: companyAccess.OBJECTS_MONITORING_REMOVAL,
    })

    property bool maintenanceReportAvailable: {
        !!appCompany
        && !!appCompany.workplaces_model
        && !!appCompany.workplaces_model.incidents_settings
        && !!appCompany.workplaces_model.incidents_settings.maintenance_report_settings
        && appCompany.workplaces_model.incidents_settings.maintenance_report_settings.report_enabled === "ON"
        && companyAccess.MAINTENANCE_REPORT_OBJECTS && __maintenance_report_features__
    }

    Connections {
        target: appUser

        onEmployeeRolesAccessResponse: {
            rights = appUser.employee_roles_access_rights
        }
    }

    Connections {
        target: app.bindings_module

        onMonitoringApplicationRejectSuccess: reloadModel()
    }

    Loader {
        id: loader

        anchors.fill: parent

        z: 1
    }

    Item {
        id: addObjectItem

        width: parent.width
        height: 135

        Column {
            anchors {
                horizontalCenter: parent.horizontalCenter
                verticalCenter: parent.verticalCenter
            }

            spacing: 5
            topPadding: 45

            DS3.ButtonOutlined {
                id: addObject

                width: objectsSidebar.width - 32

                anchors.horizontalCenter: parent.horizontalCenter

                visible: companyAccess.NEW_SEMIFINISHED_OBJECT_ADD || companyAccess.NEW_OBJECT_ADD
                text: tr.a911_add_object

                onClicked: {
                    // todo :: roles

                    if (companyAccess.NEW_OBJECT_ADD) {
                        Popups.add_alt_object_popup("facility")
                        return
                    }

                    if (companyAccess.NEW_SEMIFINISHED_OBJECT_ADD) {
                        Popups.add_alt_object_popup("hub")
                        return
                    }
                }
            }

            Item {
                width: objectsSidebar.width
                height: 55

                DS3.ButtonText {
                    id: maintenanceReport

                    anchors.left: parent.left

                    text: tr.maintenance_pdf_report_title
                    visible: maintenanceReportAvailable && mrRights

                    onClicked: {
                        objectsStack.objectsScreenLoaderSource = "qrc:/resources/qml/screens/home/pages/objects/maintenance_report/MaintenanceReport.qml"
                    }
                }

                DS3.ButtonText {
                    id: refreshModel

                    anchors.right: parent.right

                    text: tr.Refresh_button_desktop
                    buttonIconSource: "qrc:/resources/images/desktop/button_icons/refresh.svg"

                    onClicked: {
                        refreshAnim.start()
                        reloadModel()
                    }

                    RotationAnimator {
                        id: refreshAnim

                        target: refreshModel.animIcon
                        from: 0
                        to: 360
                        duration: 500
                    }
                }
            }
        }
    }

    Item {
        id: sidebarBody

        width: parent.width
        anchors {
            top: addObjectItem.bottom
            right: parent.right
            bottom: parent.bottom
        }

        ScrollView {
            id: scrollView

            anchors.fill: parent
            clip: true

            ScrollBar.vertical: Custom.ScrollBar {
                parent: scrollView
                anchors {
                    top: parent.top
                    right: parent.right
                    bottom: parent.bottom
                }

                policy: {
                    if (scrollView.contentHeight > scrollView.height) {
                        return ScrollBar.AlwaysOn
                    }
                    return ScrollBar.AlwaysOff
                }
            }

            ColumnLayout {
                anchors.fill: parent
                spacing: 1

                CategoriesItem {
                    id: activeTab

                    mode: "active"
                    text: tr.active_objects_911
                    selected: objectsSidebar.currentTab == activeTab
                    count: appCompany.objects_model.categories_counters.active

                    visible: enabledCategories.active

                    property var tabVisibility: null

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = activeTab
                        app.facility_module.get_category(mode, true)
                    }

                    onVisibleChanged: {
                        if (tabVisibility == null) return
                        if (tabVisibility == companyAccess.OBJECTS_ACTIVE) return

                        activeTab.tabVisibility = companyAccess.OBJECTS_ACTIVE

                        objectsSidebar.currentTab = activeTab
                        app.facility_module.get_category(activeTab.mode, true)
                    }

                    Component.onCompleted: {
                        activeTab.tabVisibility = companyAccess.OBJECTS_ACTIVE
                    }
                }

                CategoriesItem {
                    id: allInstallationObjectsTab

                    mode: "with_installation_services"
                    text: tr.all_objects_desktop
                    selected: objectsSidebar.currentTab == allInstallationObjectsTab
                    count: appCompany.objects_model.categories_counters.with_installation_services

                    /*
                        Depends on Active-Tab visibility.
                    */
                    visible: enabledCategories.with_installation_services && !enabledCategories.active

                    property var tabVisibility: null

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = allInstallationObjectsTab
                        app.facility_module.get_category(mode, true)
                    }

                    onVisibleChanged: {
                        if (companyAccess.OBJECTS_ACTIVE) return

                        if (tabVisibility == null) return
                        if (tabVisibility == companyAccess.OBJECTS) return

                        allInstallationObjectsTab.tabVisibility = companyAccess.OBJECTS

                        objectsSidebar.currentTab = allInstallationObjectsTab
                        app.facility_module.get_category(allInstallationObjectsTab.mode, true)
                    }

                    Component.onCompleted: {
                        allInstallationObjectsTab.tabVisibility = companyAccess.OBJECTS
                    }
                }

                CategoriesItem {
                    id: armTab

                    mode: "armed"
                    text: tr.on_guard_objects_911
                    selected: objectsSidebar.currentTab == armTab
                    count: appCompany.objects_model.categories_counters.armed

                    visible: enabledCategories.armed

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = armTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: disarmTab

                    mode: "disarmed"
                    text: tr.not_guarded_objects_911
                    selected: objectsSidebar.currentTab == disarmTab
                    count: appCompany.objects_model.categories_counters.disarmed

                    visible: enabledCategories.disarmed

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = disarmTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: sleepTab

                    mode: "sleep"
                    text: tr.sleep_mode_objects_911
                    selected: objectsSidebar.currentTab == sleepTab
                    count: appCompany.objects_model.categories_counters.sleep

                    visible: enabledCategories.sleep

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = sleepTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    color: ui.colors.dark3
                    lHeight: 16
                    visible: sleepTab.visible
                }

                CategoriesItem {
                    id: offlineTab

                    mode: "offline"
                    text: tr.offline
                    selected: objectsSidebar.currentTab == offlineTab
                    count: appCompany.objects_model.categories_counters.offline

                    visible: enabledCategories.offline

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = offlineTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: problemTab

                    mode: "warnings"
                    text: tr.a911_problems
                    attention: true
                    selected: objectsSidebar.currentTab == problemTab
                    count: appCompany.objects_model.categories_counters.warnings

                    visible: enabledCategories.warnings

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = problemTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: noAgreementTab

                    mode: "no_agreement"
                    text: tr.a911_without_contract
                    selected: objectsSidebar.currentTab == noAgreementTab
                    count: appCompany.objects_model.categories_counters.no_agreement

                    visible: enabledCategories.no_agreement

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = noAgreementTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    visible: withInstallationServicesTab.visible
                    color: ui.colors.dark3
                    lHeight: 16
                    Layout.fillHeight: true
                }

                CategoriesItem {
                    id: withInstallationServicesTab

                    mode: "with_installation_services"
                    text: tr.objects_only_installation
                    selected: objectsSidebar.currentTab == withInstallationServicesTab
                    count: appCompany.objects_model.categories_counters.with_installation_services

                    /*
                        Depends on AllInstallationObjects-Tab visibility.
                    */
                    visible: enabledCategories.with_installation_services && !allInstallationObjectsTab.visible

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = withInstallationServicesTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                Rectangle {
                    id: monitoringTitle

                    /*
                        Depends on AllInstallationObjects-Tab visibility.
                    */
                    visible: companyAccess.OBJECTS_MONITORING_REQUEST_FROM_INSTALLER && !(companyAccess.OBJECTS && !companyAccess.OBJECTS_ACTIVE)
                    color: ui.colors.dark3

                    Layout.minimumHeight: 40
                    Layout.minimumWidth: parent.width

                    DS.TextBodyMBold {
                        text: tr.monitoring_requests_filter
                        anchors {
                            left: parent.left
                            leftMargin: 24
                            bottom: parent.bottom
                        }
                    }
                }

                CategoriesItem {
                    id: installersTab

                    mode: "installers"
                    text: tr.requests_from_installer
                    selected: objectsSidebar.currentTab == installersTab
                    count: appCompany.objects_model.categories_counters.installers

                    visible: enabledCategories.installers

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = installersTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: connectTab

                    mode: "connect"
                    text: tr.a911_connection_requests
                    selected: objectsSidebar.currentTab == connectTab
                    count: appCompany.objects_model.categories_counters.connect

                    visible: enabledCategories.connect

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = connectTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: disconnectTab

                    mode: "disconnect"
                    text: tr.disconnection_requests_911
                    selected: objectsSidebar.currentTab == disconnectTab
                    count: appCompany.objects_model.categories_counters.disconnect

                    visible: enabledCategories.disconnect

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = disconnectTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    id: trashTab

                    mode: "trash"
                    text: tr.a911_to_delete
                    selected: objectsSidebar.currentTab == trashTab
                    count: appCompany.objects_model.categories_counters.trash

                    visible: enabledCategories.trash

                    mouseArea.onClicked: {
                        objectsSidebar.currentTab = trashTab
                        app.facility_module.get_category(mode, true)
                    }
                }

                CategoriesItem {
                    color: ui.colors.dark3
                    lHeight: 0
                    Layout.fillHeight: true
                }
            }
        }
    }
}