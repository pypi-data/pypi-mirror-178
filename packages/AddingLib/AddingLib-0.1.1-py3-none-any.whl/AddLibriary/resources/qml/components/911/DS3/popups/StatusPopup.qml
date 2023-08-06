import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    enum StatusType {
        Spinner,
        ProgressForward
    }

//  Status type of status popup
    property var statusType: StatusPopup.StatusType.Spinner
//  Text of the popup
    property var description: tr.request_send
//  Timeout for closing in seconds
    property int timeout
//  List of signal to finalize on it
    property var endSignals: []
//  List of signals to update progress
    property var progressUpdateSignals: []
//  Steps need to complete progress
    property int stepsAmount: progressForward.stepsAmount

    function finalize() {
        if (!endSignals || !endSignals.length) {
            spinner.finalize()
            aboutToHideTimer.start()
        }
    }

    function customEndSignalFinalize() {
        spinner.finalize()
        aboutToHideTimer.start()
    }

    function updateProgress() {
        progressForward.update()
        if (progressForward.value == 100) {
            statusType = StatusPopup.StatusType.Spinner
            spinner.finalize()
            aboutToHideTimer.start()
        }
    }

    Component.onCompleted: {
        timeoutTimer.start()

        if (!!popup.endSignals)
            for (var i = 0; i < popup.endSignals.length; i++) {
                popup.endSignals[i].connect(popup.customEndSignalFinalize)
            }
        if (!!popup.progressUpdateSignals)
            for (var i = 0; i < popup.progressUpdateSignals.length; i++) {
                popup.progressUpdateSignals[i].connect(popup.updateProgress)
            }
    }

    Component.onDestruction: {
        if (!!popup.endSignals)
            for (var i = 0; i < popup.endSignals.length; i++) {
                popup.endSignals[i].disconnect(popup.customEndSignalFinalize)
            }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.finalize()
        }

        onActionFailed: {
            popup.close()
        }

        onGetDonorHubDataSuccess: {
            popup.close()
        }

        onChangedGroupModeSuccess: {
            popup.finalize()
        }

        onMigrationErrorsSignal: {
            popup.close()
        }

        onDeviceNetworkCommandError: {
            popup.finalize()
        }

        onDeviceNetworkCommandSuccess: {
            popup.finalize()
        }

        onHubGSMActionSuccess: {
            popup.finalize()
        }

        onSetEthernetFailed: {
            popup.close()
        }
    }

    Connections {
        target: app.hub_management_module

        onScenarioSuccess: {
            popup.finalize()
        }

        onDelScenarioSuccess: {
            popup.finalize()
        }

        onSaveDCOSensorSuccess: {
            popup.finalize()
        }

        onDeleteWithCardStarted: {
            popup.finalize()
        }

        onFormatAccessCardStarted: {
            popup.finalize()
        }

        onPressKeypadButton: {
            popup.finalize()
        }

        onBypassActionSuccess: {
            popup.finalize()
        }
    }

    Connections {
        target: ezviz

        onEzvizActionSuccess: {
            popup.finalize()
        }

        onEzvizActionFailed: {
            popup.close()
        }
    }

    Connections {
        target: appUser

        onEmployeeRolesAccessResponse: {
            popup.close()
        }
    }

    width: 286

    hasCrossButton: false
    closePolicy: Popup.NoAutoClose

    DS3.Spinner {
        id: spinner

        anchors.horizontalCenter: parent.horizontalCenter

        visible: statusType == StatusPopup.StatusType.Spinner
    }

    DS3.ProgressForward {
        id: progressForward

        anchors.horizontalCenter: parent.horizontalCenter

        visible: statusType == StatusPopup.StatusType.ProgressForward
    }

    DS3.Spacing {
        height: 16
    }

    DS3.Text {
        width: parent.width

        text: popup.description
        style: ui.ds3.text.title.XSBold
        horizontalAlignment: Text.AlignHCenter
    }

    Timer {
        id: aboutToHideTimer

        interval: 1500

        onTriggered: {
            popup.close()
        }
    }

    Timer {
        id: timeoutTimer

        interval: 1000 * timeout

        onTriggered: {
            popup.close()
        }
    }
}