import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: companyInfo

    property var companyData
//  Object with states of access toggles
    readonly property var accessToggles: companyData.access_toggles

    color: ui.ds3.bg.base

    function rollback() {
        systemSettings.checked = accessToggles.arm_disarm_settings_access
        panic.checked = accessToggles.panic_settings_access
        viewCameras.checked = accessToggles.camera_settings_access
        switchControls.checked = accessToggles.relay_settings_access
        chimeActivation.checked = accessToggles.chimes_activation_access
    }

    Connections {
        target: app.hub_management_module

        onInstallationCompanyDeleted: {
            companyInfoLoader.source = ""
        }
        onInstallationCompanyPermissionsUpdateSuccess: companyAccessChangesChecker.changeInitialValues()
        onInstallationCompanyPermissionsUpdateFailed: rollback()
        onInstallationCompanyPermissionsCancellationSuccess: {
            systemSettings.checked = false
            panic.checked = false
            viewCameras.checked = false
            switchControls.checked = false
            chimeActivation.checked = false
            companyAccessChangesChecker.changeInitialValues()
        }
    }

    Connections {
        target: app.facility_module

        onAnotherInstallationCompanyDeleted: {
            companyInfoLoader.source = ""
        }
    }

    DS3.ChangesChecker {
        id: companyAccessChangesChecker

        listeningValues: [
            systemSettings.checked,
            panic.checked,
            viewCameras.checked,
            switchControls.checked,
            chimeActivation.checked
        ]
    }

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    DS3.NavBarModal {
        id: companyInfoBar

        headerText: companyData.name
        showCloseIcon: false
        isRound: false
        showBackArrow: true

        onBackAreaClicked: {
            companyInfoLoader.source = ""
        }
    }

    DS3.ScrollView {
        id: scrollView

        anchors {
            fill: undefined
            top: companyInfoBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Spacing {
            height: 24
        }

        DS3.CompanyImage {
            width: 136
            height: 136

            anchors.horizontalCenter: parent.horizontalCenter

            name: companyData.name
            source: (companyData.logo.images.filter(
                    (image) => image.resolution == "300x300"
                )[0] || {"url": ""}).url
        }

        DS3.Spacing {
            height: 48
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            Repeater {
                model: companyData.phone_numbers ? companyData.phone_numbers : []

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: modelData.description ? modelData.description : tr.company_phone_number
                    atomTitle.subtitle: modelData.number ? modelData.number : ""
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"

                    onRightControlClicked: {
                        util.set_clipboard_text(atomTitle.subtitle)
                    }
                }
            }

            Repeater {
                model: companyData.customer_inquiries_emails ? companyData.customer_inquiries_emails : []

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: tr.email
                    atomTitle.subtitle: modelData.email ? modelData.email : ""
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/Shape-M.svg"
                    buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"

                    onRightControlClicked: {
                        util.set_clipboard_text(atomTitle.subtitle)
                    }
                }
            }

            DS3.InfoTitleButtonIcon {
                atomTitle.title: tr.website
                atomTitle.subtitle: companyData.website_url ? companyData.website_url : ""
                visible: !!companyData.website_url
                leftIcon.source: "qrc:/resources/images/Athena/common_icons/Connection-M.svg"
                buttonIcon.source: "qrc:/resources/images/Athena/common_icons/ExternalLink-M.svg"

                onRightControlClicked: {
                    Qt.openUrlExternally(atomTitle.subtitle)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            width: parent.width

            text: tr.available_in_alt + ":"
            isBgTransparent: true
            isCaps: true
            forceTextToLeft: true
            visible: !!companyData.locations
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InfoTitle {
                width: parent.width

                atomTitle.title: util.join(companyData.locations, "")
                visible: !!companyData.locations
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            width: parent.width

            text: tr.permissions
            isBgTransparent: true
            isCaps: true
            forceTextToLeft: true
            visible: !!companyData.locations
        }

        //--------------------- permissions --------------------------------------
        DS3.SettingsContainer {
            id: permissionsContainer

            width: parent.width

            DS3.SettingsSwitch {
                id: systemSettings

                title: tr.arm_disarm
                checked: accessToggles.arm_disarm_settings_access
            }

            DS3.SettingsSwitch {
                id: panic

                title: tr.panic
                checked: accessToggles.panic_settings_access
            }

            DS3.SettingsSwitch {
                id: viewCameras

                visible: !hub.access_to_camera_privacy_settings_allowed
                title: tr.view_cameras
                checked: accessToggles.camera_settings_access
            }

            DS3.SettingsSwitch {
                id: switchControls

                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS"
                title: tr.switch_controls
                checked: accessToggles.relay_settings_access
            }

            DS3.SettingsSwitch {
                id: chimeActivation

                visible: hub.chimes_available
                enabled: devEnable
                title: tr.chime_activation
                checked: accessToggles.chimes_activation_access
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.ButtonRow {
                id: cancelAccessBtn

                isDanger: true
                text: tr.cancel_access
                enabled: devEnable

                onClicked: {
                    Popups.please_wait_popup()
                    app.hub_management_module.cancel_installation_company_permissions(hub.id, companyData.company_hex_id)
                }
            }

            DS3.ButtonRow {
                id: deleteUserButton

                isDanger: true
                text: tr.decline_services_installer

                onClicked: Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.decline_services_installer_title,
                        text: tr.decline_services_installer_descr,
                        firstButtonText: tr.decline_services_installer_button,
                        firstButtonCallback: () => {
                            appCompany.current_facility
                                ? app.facility_module.delete_installation_service_on_hub(facility.hub_id, companyData.company_hex_id)
                                : app.hub_management_module.delete_installation_service_on_hub(hub.hub_id, companyData.company_hex_id)
                        },
                        isFirstButtonRed: true,
                        secondButtonText: tr.cancel,
                        secondButtonIsOutline: true,
                        isVertical: true
                    }
                )
            }
        }

        DS3.InfoFooter {
            footerType: DS3.InfoFooter.FooterType.User
            subtitleUpper.text: `${tr.company_id} ${management.users.get_user(companyData.company_hex_id).index}`
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors.bottom: parent.bottom

        buttonText: tr.save
        hasBackground: true
        enabled: companyAccessChangesChecker.hasChanges

        button.onClicked: {
            Popups.please_wait_popup()
            app.hub_management_module.update_installation_company_permissions(
                hub.id,
                companyData.company_hex_id,
                {
                    arm_disarm_settings_access: systemSettings.checked,
                    panic_settings_access: panic.checked,
                    camera_settings_access: viewCameras.checked,
                    relay_settings_access: switchControls.checked,
                    chimes_activation_access: chimeActivation.checked
                },
                companyData.company_hub_permissions
            )
        }
    }
}
