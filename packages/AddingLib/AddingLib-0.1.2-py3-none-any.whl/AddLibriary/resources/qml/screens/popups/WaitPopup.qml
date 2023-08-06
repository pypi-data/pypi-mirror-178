import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/animations/" as Anime

AjaxPopup {
    id: popup
    objectName: "waitPopup"
    modal: true
    closePolicy: Popup.NoAutoClose

    Rectangle {
        width: 128
        height: 128
        anchors.centerIn: parent
        radius: 8
        color: ui.colors.dark4
        opacity: 0.8
        border.color: "black"
        border.width: 1

        Anime.PulseAnimation {
            barCount: 3
            width: 64
            height: 64
            color: ui.colors.green1
            anchors.centerIn: parent
        }
    }

    Timer {
        id: timer
        running: false
        repeat: false
        interval: 300
        onTriggered: {
            popup.close()
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            timer.start()
        }

        onActionFailed: {
            timer.start()
        }
    }
    Connections {
        target: app.login_module

        onLoginSuccess: {
            timer.start()
        }

        onProLoginSuccess: {
            timer.start()
        }

        onLoginFailed: {
            timer.start()
        }

        onIsNotConfirmed: {
            timer.start()
        }

        onConfirmTotpFailed: {
            timer.start()
        }

        onEnterVerificationCode: {
            timer.start()
        }
    }
}


