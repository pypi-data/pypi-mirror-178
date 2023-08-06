import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    property string deviceCalibrationStatus: device.calibration_status
    property string uiCalibrationStatus: "READY"

    Component.onDestruction: if ([
        "WAITING_FOR_DIALOG",
        "WAITING_FOR_START",
        "IN_PROGRESS"
    ].includes(deviceCalibrationStatus))
        app.hub_management_module.device_command(device, 35)

    onDeviceCalibrationStatusChanged: {
        if (deviceCalibrationStatus == "IN_PROGRESS") uiCalibrationStatus = "IN_PROGRESS"
        else if (["WAITING_FOR_START", "WAITING_FOR_DIALOG"].includes(deviceCalibrationStatus)) uiCalibrationStatus = "STARTING"
        else if (deviceCalibrationStatus == "WAITING_FOR_FINISH") uiCalibrationStatus = "STOPPING"
        else if (["NO_CALIBRATION", "NO_CALIBRATION_STATE_INFO"].includes(deviceCalibrationStatus))
            uiCalibrationStatus = uiCalibrationStatus == "IN_PROGRESS" ? "COMPLETED" : "READY"
    }

    onUiCalibrationStatusChanged: {
        if (["READY", "STOPPING", "STARTING"].includes(uiCalibrationStatus)) calibrationTimer.stop()
        else if (uiCalibrationStatus == "IN_PROGRESS") calibrationTimer.start()
        else if (uiCalibrationStatus == "COMPLETED" && !calibrationTimer.finished) calibrationTimer.finish()
    }

    width: parent.width

    title: tr.calibration_lq_title
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    Item {
        width: 48
        height: 48

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.Icon {
            anchors.centerIn: parent

            source: "qrc:/resources/images/Athena/common_icons/ServiceSettings-M.svg"
            color: ui.ds3.figure.base
        }
    }

    DS3.InfoContainer {
        width: parent.width

        titleComponent.text: device.name
        descComponent.text: device.info_name
    }

    DS3.Spacing {
        height: 24
    }

    DS3.ProgressCountdownM {
        id: calibrationTimer

        anchors.horizontalCenter: parent.horizontalCenter

        finishedText: tr.completed_state
        autoFinish: false
    }

    DS3.Spacing {
        height: 16
    }

    DS3.SettingsContainer {
        width: parent.width - 32

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.CommentImportant {
            width: parent.width

            imageItem.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
            atomTitle.subtitle: ({
                "READY": tr.calibration_lq_descr_before,
                "IN_PROGRESS": tr.calibration_lq_descr_progress,
                "COMPLETED": tr.calibration_lq_descr_after,
                "STARTING": tr.calibration_lq_descr_progress,
                "STOPPING": tr.calibration_lq_descr_progress,
            })[uiCalibrationStatus]
        }
    }

    footer: DS3.ButtonBar {
        hasComment: true
        hasBackground: true
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        commentText: ({
            "READY": tr.ready,
            "IN_PROGRESS": tr.in_progress_now,
            "COMPLETED": tr.ready,
            "STARTING": tr.preparing_for_test_calibration,
            "STOPPING": tr.stopping_the_progress,
        })[uiCalibrationStatus]
        enabled: !["STARTING", "STOPPING"].includes(uiCalibrationStatus)
        button {
            text: ({
                "READY": tr.start,
                "IN_PROGRESS": tr.stop,
                "COMPLETED": tr.start,
                "STARTING": tr.stop,
                "STOPPING": tr.start,
            })[uiCalibrationStatus]
            isOutline: uiCalibrationStatus == "IN_PROGRESS"
            onClicked: {
                if (uiCalibrationStatus == "IN_PROGRESS") {
                    Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                        {
                            title: tr.stop_calibration_title,
                            text: tr.stop_calibration_descr,
                            firstButtonText: tr.stop,
                            secondButtonText: tr.continue_,
                            firstButtonCallback: () => {
                                Popups.waitPopup(deviceCalibrationStatusChanged, {timeout: 180})
                                calibrationTimer.stop()
                                app.hub_management_module.device_command(device, 35)
                            }
                        }
                    )
                } else {
                    Popups.waitPopup(deviceCalibrationStatusChanged, {timeout: 180})
                    app.hub_management_module.device_command(device, 34)
                }
            }
        }
    }
}