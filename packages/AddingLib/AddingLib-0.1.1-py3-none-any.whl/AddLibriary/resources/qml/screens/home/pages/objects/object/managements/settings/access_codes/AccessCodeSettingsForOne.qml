import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


Rectangle {
    property var accessCode: null
    property string passwordForSaving
    property string duressPasswordForSaving
    property var localDuressPassHashExist: accessCode.duress_pass_hash_exist

    Connections {
        target: app.rpc.hubAccessCodes

        onAccessCodeDeleted: loaderAccessCode.source = ""
        onAccessCodesSettingsUpdatedFailed: {
            DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.failed_save_changes,
                text: errorText == "NOT_UNIQUE" ? tr.failed_save_changes_code_validation : tr.failed_save_id_access_code,
                firstButtonText: tr.i_will_check,
                secondButtonCallback: () => {
                    loaderAccessCode.source = ""
                    loaderAccessCode.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/AccessCodeSettingsForOne.qml", {"accessCode": accessCode})
                },
                secondButtonText: tr.rollback_changes,
                secondButtonIsOutline: true,
                isSecondButtonRed: true,
                isVertical: true,
            })
        }
    }

    Connections {
        target: app

        onActionSuccess: changesChecker.changeInitialValues()
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.code_settings_title
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            if (buttonBar.enabled) {
                var discard_changes_popup = DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                    title: tr.dont_save_title,
                    text: tr.dont_save_descr,
                    firstButtonText: tr.discard_changes_button,
                    isFirstButtonRed: true,
                    firstButtonCallback: () => {
                        loaderAccessCode.source = ""
                        isDiscardChanges = false
                    },
                    secondButtonCallback: () => {
                        discard_changes_popup.close()
                    },
                    secondButtonText: tr.back_editing_button,
                    secondButtonIsOutline: true,
                    isVertical: true,
                })
            } else loaderAccessCode.source = ""
        }
    }

    DS3.ScrollView {
        id: contentScrollView

        width: parent.width

        anchors {
            fill: undefined
            top: navBarModal.bottom
            topMargin: 1
            bottom: buttonBar.top
            bottomMargin: 1
        }

        padding: 24

        DS3.SettingsContainer {
            DS3.InputSingleLine {
                id: nameInput

                atomInput {
                    label: tr.name
                    placeholderText: tr.access_code_name_input
                    text: accessCode.name

                    onTextChanged: atomInput.text = util.validator(atomInput.text, 24)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.InputPicker {
                id: index

                width: parent.width

                model: context.indexModel
                notIncludedErrorText: tr.value_out_of_range
                currentIndex: accessCode ? model.indexOf(accessCode.index) : -1
                input {
                    hasValidationOnFocusLost: false
                    regex: /[0-9]{3}/
                    atomInput {
                        label: tr.user_id_access_code_title
                        text: accessCode.index
                    }
                }
            }
        }

        DS3.Comment {
            text: tr.user_id_access_code_descr
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            text: tr.passcodes_plural
            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
        }

        DS3.SettingsContainer {
            DS3.SettingsNavigationTitlePrimary {
                id: password

                title: tr.access_code_title

                onEntered: DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/ChangeAccessCodePasswordPopup.qml",
                    {"duressPassword": false, "accessCode": accessCode}
                )
            }

            DS3.ButtonRow {
                id: addDuressButton

                width: parent.width

                text: tr.add_duress_code
                visible: accessCode && !localDuressPassHashExist
                rowLeftAlign: true

                onClicked: DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/ChangeAccessCodePasswordPopup.qml",
                    {"duressPassword": true, "accessCode": accessCode}
                )
            }

            DS3.SettingsNavigationTitlePrimary {
                id: duress_password

                title: tr.duress_code_new
                visible: accessCode && localDuressPassHashExist

                onEntered: DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/ChangeAccessCodePasswordPopup.qml",
                    {"duressPassword": true, "accessCode": accessCode}
                )
            }
        }

        DS3.Spacing {
            height: 24

            visible: security_management.visible
        }

        DS3.SettingsContainer {
            DS3.SettingsTitleSecondaryNavigation {
                id: security_management

                visible: hub.groups_enabled
                title: tr.arm_permission_with_group
                subtitle: {
                    if (!accessCode) return ""
                    var counterOfActiveGroups = 0
                    for (var index = 0; index < management.groups.length; index++) {
                        accessCode.group_permissions.forEach((accessCodeGroup) => {
                            if (management.groups.get(index).id == accessCodeGroup.group_id) {
                                counterOfActiveGroups += 1
                            }
                        })
                    }
                    var counterOfAllGroups = management.groups.length
                    var isNightModeActive = accessCode.arming_permissions.includes("ACCESS_CODE_ARMING_PERMISSION_NIGHT_MODE")

                    if (isNightModeActive) {
                        if (counterOfActiveGroups == 0) return tr.perimeter_armed
                        if (counterOfActiveGroups == counterOfAllGroups) return tr.full_hub_access
                        if (counterOfActiveGroups != counterOfAllGroups) return tr.partial_access
                    } else {
                        if (counterOfActiveGroups == 0) return tr.no_hub_access
                        if (counterOfActiveGroups == counterOfAllGroups) return tr.not_assigned
                        if (counterOfActiveGroups != counterOfAllGroups) return util.insert(tr.scenario_arm_disarm_groups_selected, [counterOfActiveGroups])
                    }
                }

                onEntered: {
                    if (buttonBar.enabled) {
                        var discard_changes_popup = DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                            title: tr.changes_not_saved,
                            text: tr.changes_not_saved_descr,
                            firstButtonText: tr.discard_changes_button,
                            isFirstButtonRed: true,
                            firstButtonCallback: () => {
                                loaderAccessCode.setSource(
                                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/AccessCodeSecurityManagement.qml",
                                    {"accessCode": accessCode}
                                )
                                isDiscardChanges = false
                            },
                            secondButtonCallback: () => {
                                discard_changes_popup.close()
                            },
                            secondButtonText: tr.back_editing_button,
                            secondButtonIsOutline: true,
                            isVertical: true,
                        })
                        return
                    }
                    loaderAccessCode.setSource(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/AccessCodeSecurityManagement.qml",
                        {"accessCode": accessCode}
                    )
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.ButtonRow {
                width: parent.width

                text: accessCode && accessCode["enabled"] ? tr.deactivate_access_code : tr.activate_access_code
                isDanger: accessCode && accessCode["enabled"]

                onClicked: {
                    DesktopPopups.waitPopup(app.rpc.hubAccessCodes.accessCodeStateUpdated, changesChecker.changeInitialValues)
                    context.updateAccessCodeState(accessCode.id, !accessCode.enabled)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.ButtonRow {
                text: tr.delete_access_code
                isDanger: true

                onClicked: {
                    var deletePopup = DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                        title: tr.delete_access_code_title,
                        text: tr.delete_access_code_descr,
                        firstButtonText: tr.delete,
                        isFirstButtonRed: true,
                        firstButtonCallback: () => {
                            context.deleteAccessCode(accessCode.id)
                            deletePopup.isLoading = true
                        },
                        secondButtonText: tr.cancel,
                        secondButtonIsOutline: true,
                        isVertical: true,
                    })
                }
            }
        }
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            nameInput.atomInput.text,
            index.input.atomInput.text,
            passwordForSaving,
            duressPasswordForSaving
        ]
    }

    DS3.ButtonBar {
        id: buttonBar

        anchors.bottom: parent.bottom

        enabled: changesChecker.hasChanges && nameInput.atomInput.text != ""
        buttonText: tr.save
        hasBackground: true
        button.onClicked: {
            DesktopPopups.waitPopup(
                app.rpc.hubAccessCodes.accessCodesSettingsUpdated,
                changesChecker.changeInitialValues,
                {
                    failSignal: app.rpc.hubAccessCodes.accessCodesSettingsUpdatedFailed,
                }
            )

            var settings = {}
            settings["id"] = accessCode.id
            settings["name"] = {"name": nameInput.atomInput.text.trim()}
            settings["index"] = Number.parseInt(index.input.atomInput.text)
            if (passwordForSaving) settings["pass_hash"] = passwordForSaving
            if (duressPasswordForSaving) settings["duress_pass_hash"] = duressPasswordForSaving
            context.updateSettings(settings)
        }

        onEnabledChanged: {
            isDiscardChanges = buttonBar.enabled
        }
    }
}