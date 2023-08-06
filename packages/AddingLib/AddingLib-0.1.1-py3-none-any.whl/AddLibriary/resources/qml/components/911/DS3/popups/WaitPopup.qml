import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

//  Text of the popup
    property var description
//  Timeout for closing in seconds
    property int timeout
//  Signal to finalize on it
    property var waitSignal: null
//  Signal to close on it
    property var failSignal: null
//  Callback on popup close if waiting signal has been emitted
    property var waitCallback
//  Callback on popup close if waiting signal has been emitted
    property var failCallback

    function finalize() {
        spinner.finalize()
        aboutToHideTimer.start()
    }

    Component.onCompleted: {
        timeoutTimer.start()

        waitSignal.connect(popup.finalize)
        if (!!failSignal) {
            failSignal.connect(popup.close)
            if (!!popup.failCallback) failSignal.connect(popup.failCallback)
        }
    }

    Component.onDestruction: {
        waitSignal.disconnect(popup.finalize)
        if (!!failSignal) {
            failSignal.disconnect(popup.close)
            if (!!popup.failCallback) failSignal.disconnect(popup.failCallback)
        }
    }

    width: 300

    hasCrossButton: false
    closePolicy: Popup.NoAutoClose

    DS3.Spinner {
        id: spinner

        anchors.horizontalCenter: parent.horizontalCenter
    }

    DS3.Spacing {
        height: 16
    }

    DS3.Text {
        width: parent.width

        text: popup.description || tr.request_send
        style: ui.ds3.text.title.XSBold
        horizontalAlignment: Text.AlignHCenter
    }

    Timer {
        id: aboutToHideTimer

        interval: 1500

        onTriggered: {
            popup.close()
            if (!!waitCallback) waitCallback()
        }
    }

    Timer {
        id: timeoutTimer

        interval: 1000 * (timeout || 30)

        onTriggered: {
            popup.close()
        }
    }
}
