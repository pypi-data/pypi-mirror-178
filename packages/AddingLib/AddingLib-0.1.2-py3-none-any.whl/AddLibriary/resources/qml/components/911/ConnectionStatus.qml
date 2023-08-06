import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Item {
    width: 44
    height: 44
    anchors.centerIn: parent

    Rectangle {
        width: 24
        height: 24
        radius: height / 2
        anchors.centerIn: parent
        color: app.online ? ui.colors.green1 : ui.colors.red1

        Custom.HandMouseArea {
            cursorShape: Qt.ArrowCursor
            pressAndHoldInterval: 5000

            onPressAndHold: {
                Popups.internal_crash_popup()
            }
        }
    }

    Connections {
        target: app.login_module

        onLogoutSignal: {
            app.login_module.logout()
            screenLoader.source = "qrc:/resources/qml/screens/login/Login.qml"
        }
    }


    /* -------------------------------------------------------------------- */
    /* desktop tests */
    Item {
        id: accountStorage

        Accessible.name: "account_storage"
        Accessible.description: appUser.company_id ? "account:company_" + appUser.company_id : "account:pro"
        Accessible.role: Accessible.Desktop
    }
    /* -------------------------------------------------------------------- */
}
