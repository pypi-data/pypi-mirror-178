import QtQuick 2.7
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/popups.js" as Popups


Rectangle {
    id: navBarMain


//  Current or last chosen monitoring folder
    property var monitoringFolder: null
    property var currentFolder: null

    width: parent.width
    height: __figma_46_headers_features__ ? 64 : 0

    visible: __figma_46_headers_features__
    color: ui.ds3.bg.lowest

    Component.onCompleted: {
        monitoringFolder = tr.a911_incidents
        if (companyAccess.MONITORING) { currentFolder = monitoringFolder }
        else if (companyAccess.JOURNAL) { currentFolder = tr.a911_list }
        else if (companyAccess.OBJECTS) { currentFolder = tr.a911_objects }
        else if (companyAccess.COMPANY) { currentFolder = tr.a911_company }
    }

    DS3.Image {
        id: logoPro

        anchors{
            left: parent.left
            verticalCenter: parent.verticalCenter
        }

        sourceSize.width: 64
        sourceSize.height: 64
        source: "qrc:/resources/images/icons/a-logo-pro.svg"
    }

    Row {
        anchors{
            left: logoPro.right
            leftMargin: 16
        }

        visible: appUser.company_id

        DS3.CompanyNavigationTop {
            id: monitoringNavButton

            visible: companyAccess.MONITORING
            navigationImageSource: "qrc:/resources/images/Athena/notifications/Monitoring-M.svg"
            navigationText: tr.monitoring
            isSelected:  [tr.monitoring, tr.a911_incidents, tr.a911_in_processing, tr.a911_sleeping].includes(currentFolder)

            DS3.MouseArea {
                onClicked: {
                    application.debug("company -> sidebar -> monitoring")
                    if (!loaded) { loaded = true }
                    header.currentState = 0
                    currentFolder = monitoringFolder
                }
            }
        }

        DS3.CompanyNavigationTop {
            id: notificationsNavButton

            visible: companyAccess.JOURNAL
            navigationImageSource: "qrc:/resources/images/Athena/notifications/Notifications-M.svg"
            navigationText: tr.a911_list
            isSelected: currentFolder == tr.a911_list

            DS3.MouseArea {
                onClicked: {
                    application.debug("company -> sidebar -> journal")
                    if (!loaded) { loaded = true }
                    app.journal_module.get_log_entries_count()
                    header.currentState = 1
                    currentFolder = tr.a911_list
                }
            }
        }

        DS3.CompanyNavigationTop {
            id: objectsNavButton

            visible: companyAccess.OBJECTS
            navigationImageSource: "qrc:/resources/images/Athena/notifications/Object-M.svg"
            navigationText: tr.a911_objects
            isSelected: currentFolder == tr.a911_objects

            DS3.MouseArea {
                onClicked: {
                    application.debug("company -> sidebar -> facilities")
                    if (!loaded) { loaded = true }
                    app.company_module.get_company_settings()
                    header.currentState = 2
                    currentFolder = tr.a911_objects
                }
            }
        }

        DS3.CompanyNavigationTop {
            id: companyNavButton

            visible: companyAccess.COMPANY
            navigationImageSource: "qrc:/resources/images/Athena/notifications/SecurityCompany-M.svg"
            navigationText: tr.a911_company
            isSelected: currentFolder == tr.a911_company

            property var loaded: false

            DS3.MouseArea {
                onClicked: {
                    application.debug("company -> sidebar -> facilities")
                    if (!companyNavButton.loaded) {
                        companyNavButton.loaded = true
                        app.fast_response_team_module.start_staff_gbr_stream()
                    }

                    app.company_module.get_company_settings()
                    header.currentState = 3
                    currentFolder = tr.a911_company
                }
            }
        }
    }

    Row {
        id: centerRow

        anchors.centerIn: parent

        spacing: 4

        visible: appUser.company_id

        DS3.ButtonContainedRect {
            anchors.verticalCenter: parent.verticalCenter

            badge{
                text: appCompany.incidents_model.new_and_viewing_count == 0 ? "" : appCompany.incidents_model.new_and_viewing_count
                color: ui.ds3.figure.attention
            }
            color: currentFolder == tr.a911_incidents ?
                ui.ds3.bg.base :
                ui.ds3.bg.highest
            text: tr.a911_incidents
            status: DS3.ButtonRect.Status.Secondary

            onClicked: {
                application.debug("company -> header -> 'new' toggle")
                header.sidebarVisible = false
                header.currentState = 0
                if (currentIncidentsModel == appCompany.filtered_new_or_viewing_incidents_model) { return }
                currentId = null
                currentIncidentsModel = appCompany.filtered_new_or_viewing_incidents_model
                currentFolder = tr.a911_incidents
                monitoringFolder = tr.a911_incidents
            }
        }

        DS3.ButtonContainedRect {
            anchors.verticalCenter: parent.verticalCenter

            badge.text: appCompany.incidents_model.processing_count == 0 ? "" : appCompany.incidents_model.processing_count
            text: tr.a911_in_processing
            status: DS3.ButtonRect.Status.Secondary
            color: currentFolder == tr.a911_in_processing ?
                ui.ds3.bg.base :
                ui.ds3.bg.highest

            onClicked: {
                application.debug("company -> header -> 'in progress' toggle")
                header.sidebarVisible = false
                header.currentState = 0
                if (currentIncidentsModel == appCompany.filtered_processing_incidents_model) { return }
                currentId = null
                currentIncidentsModel = appCompany.filtered_processing_incidents_model
                currentFolder = tr.a911_in_processing
                monitoringFolder = tr.a911_incidents
            }
        }

        DS3.ButtonContainedRect {
            anchors.verticalCenter: parent.verticalCenter

            badge.text: appCompany.incidents_model.slept_count == 0 ? "" : appCompany.incidents_model.slept_count
            text: tr.a911_sleeping
            status: DS3.ButtonRect.Status.Secondary
            color: currentFolder == tr.a911_sleeping ?
                ui.ds3.bg.base :
                ui.ds3.bg.highest

            onClicked: {
                application.debug("company -> header -> 'sleep mode' toggle")
                header.sidebarVisible = false
                header.currentState = 0
                if (currentIncidentsModel == appCompany.filtered_snoozing_incidents_model) { return }
                currentId = null
                currentIncidentsModel = appCompany.filtered_snoozing_incidents_model
                currentFolder = tr.a911_sleeping
                monitoringFolder = tr.a911_incidents
            }
        }
    }

    Row {
        id: rightRow

        anchors{
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        spacing: 16

        DS3.ButtonContainedRect {
            anchors.verticalCenter: parent.verticalCenter

            visible: !app.synced
            text: tr.attention_time_synchronization_911
            status: DS3.ButtonRect.Status.Attention
            buttonIconSource: "qrc:/resources/images/icons/panic.svg"

            onClicked: { Popups.time_sync_popup() }
        }

        DS3.ButtonContainedRect {
            anchors.verticalCenter: parent.verticalCenter

            visible: appUser.company_id && currentFolder == tr.a911_objects

            text: tr.connection_search_911
            status: DS3.ButtonRect.Status.Secondary
            buttonIconSource: "qrc:/resources/images/Athena/common_icons/Search-M.svg"

            onClicked: {
                application.debug("company -> header -> search facilities")
                Popups.facilities_search_popup(objectsStack)
            }
        }

        DS3.InputSearch {
            id: searchField

            width: 256

            anchors.verticalCenter: parent.verticalCenter

            visible: !appUser.company_id && !hubsStack.managementLoader.item  // todo update when hubList on left side of screen implemented
            frameColor: navBarMain.color
            placeholder: tr.search_name_id

            find: () => {
                if (appUser.company_id) {
                    searchField.searchFacilities()
                } else {
                    hubsStack.updateFilter(atomInput.text)
                }
            }
        }

        DS3.ImageCircleStatus {
            id: currentUserOrCompanyImage

            property var isUserImage: {
                if (!appUser) return false
                if (!appUser.data) return false
                if (!appUser.data.user_info) return false
                if (!appUser.data.user_info.image_urls) return false
                if (!appUser.data.user_info.image_urls.base_path) return false
                return true
            }

            anchors.verticalCenter: parent.verticalCenter

            imageSource: {
                if (appUser.company_id) {
                    if (!appCompany || !appCompany.data || !appCompany.data.company_logo || !appCompany.data.company_logo.image_id || !appCompany.data.company_logo.images) return ""
                    return util.get_image_with_resolution(appCompany.data.company_logo.images, "128x128")
                } else { isUserImage ?
                    appUser.data.user_info.image_urls.base_path + appUser.data.user_info.image_urls.small :
                    ""
                }
            }

            DS3.MouseArea {
                onClicked: {
                    if (popup) {
                        popup.close()
                        popup = null
                    } else {
                        application.debug("pro -> header -> user popup")
                        parent.forceActiveFocus()
                        popup = Popups.user_popup()
                    }
                }
            }
        }
    }
}
