import QtQuick 2.12
import QtQuick.Controls 2.2


import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.Dialog {
    id: popup

    title: tr.app_restart_required_title
    text: tr.app_restart_required_descr
    isVertical: true
    firstButtonText: tr.restart_now_button
    secondButtonText: tr.later_button
    firstButtonCallback: () => {
        settings.auto_restart = true
        screenLoader.source = ""
        app.close()
        Qt.quit()
    }
}