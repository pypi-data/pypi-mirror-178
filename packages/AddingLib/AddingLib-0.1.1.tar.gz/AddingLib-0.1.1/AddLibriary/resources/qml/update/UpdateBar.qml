import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups


Item {
    id: bar
    width: parent.width
    anchors.bottom: parent.bottom
    z: 999999

    visible: updater.status == "downloading"

    Connections {
        target: updater

        onDownloadStarted: {
            // bar.visible = true
            bar.percents = 0
        }

        onDownloadSuccess: {
            // bar.visible = false
        }

        onDownloadFailed: {
            // bar.visible = false
            bar.percents = 0
        }

        onPercentsChanged: {
            bar.percents = updater.percents
        }

        onNewUpdateAvailable: {
            Popups.update_popup(update_data)
        }
    }

    property var percents: 0

    height: visible ? 3 : 0

    onPercentsChanged: {
        rect.width = percents / 100 * parent.width
    }

    Rectangle {
        id: rect
        width: 0
        height: 3
        color: ui.colors.green1

        Behavior on width {
            id: behav
            NumberAnimation { duration: 2000 }
        }
    }

    onWidthChanged: {
        var temp = percents
        behav.enabled = false
        percents = temp
        behav.enabled = true
    }

    Timer {
        repeat: true
        running: true
        interval: app.updates_time

        onTriggered: {
            updater.check_update()
            app.check_app_version()
        }
    }

    Timer {
        repeat: false
        running: true
        interval: 60000

        onTriggered: {
            updater.check_update()
        }
    }
}
