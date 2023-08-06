import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Window 2.3
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom


Window {
    id: notificationWindow

    signal loadNotification()
    signal destroyNotification()
    signal updateNotification(variant newInfo, variant newTime)

    property var notification: null

    property var stackIndex: -1
    property var startTime: null
    property var maxX: Screen.desktopAvailableWidth - 24
    property var maxY: Screen.desktopAvailableHeight - 24

    width: 300
    height: 100

    x: maxX - width
    y: maxY - height - stackIndex * (height + 12)

    flags: {
        if (__platform__ == "win32") return Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup
        if (__platform__ == "darwin") return Qt.FramelessWindowHint | Qt.ToolTip | Qt.WindowStaysOnTopHint | Qt.WA_TranslucentBackground
        return Qt.FramelessWindowHint | Qt.ToolTip | Qt.WindowStaysOnTopHint | Qt.WA_TranslucentBackground  | Qt.WA_ShowWithoutActivating | Qt.WindowDoesNotAcceptFocus
    }


    onLoadNotification: {
        /*
            Push a new notification instance
            to the notifications stack and receive stack index.
        */
        application.notifications.push(notificationWindow)
        notificationWindow.stackIndex = application.notifications.indexOf(notificationWindow)
    }

    onDestroyNotification: {
        /*
            Hide notification and reset data & timer & startTime.
        */
        notificationWindow.hide()

        notificationWindow.notification = null
        notificationWindow.startTime = null

        notificationTimer.stop()
        notificationTimer.interval = application.notificationsShowingTime
    }

    onUpdateNotification: {
        /*
            Update notification with new data & startTime & restart timer.

            newInfo - data from the previous notification.
            newTime - startTime from the previous notification.
        */
        if (!newInfo) return

        notificationTimer.stop()
        notificationTimer.interval = application.notificationsShowingTime - (new Date().getTime() - newTime)
        notificationTimer.start()

        notificationWindow.notification = newInfo
        notificationWindow.startTime = newTime

        notificationWindow.show()
    }


    Component.onCompleted: {
        notificationWindow.loadNotification()
    }

    Timer {
        id: notificationTimer

        running: false
        interval: application.notificationsShowingTime

        onTriggered: {
            notificationWindow.destroyNotification()
        }
    }


    Rectangle {
        id: notificationBody

        color: ui.colors.dark3
        anchors.fill: parent

        Custom.HandMouseArea {
            onClicked: {
                if (notificationWindow.notification && notificationWindow.notification.desktop) {

                    if (notificationWindow.notification.desktop.system) {
                        application.requestActivate()
                        application.notificationClicked()

                        app.raise_window_force()

                        return
                    }

                    if (notificationWindow.notification.desktop.hub) {
                        application.goToHubNotifications(notificationWindow.notification.desktop.hub)
                    }
                }
            }
        }

        Item {
            id: imageItem

            width: parent.width * 0.25
            height: parent.height

            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }

            Image {
                width: 64
                height: width

                source: notificationWindow.notification && notificationWindow.notification.desktop && notificationWindow.notification.desktop.image ? notificationWindow.notification.desktop.image : "qrc:/resources/images/icons/a-logo-pro.svg"
                anchors.centerIn: parent

                sourceSize {
                    width: parent.width
                    height: width
                }
            }
        }

        Item {
            id: textItem

            width: parent.width * 0.75
            height: parent.height

            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            Custom.FontText {
                text: notificationWindow.notification && notificationWindow.notification.desktop && notificationWindow.notification.desktop.text ? notificationWindow.notification.desktop.text : ""
                width: parent.width - 20
                maximumLineCount: 2
                color: ui.colors.light3
                font.pixelSize: 14
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                anchors {
                    left: parent.left
                    leftMargin: 4
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        Item {
            id: closeItem

            width: 40
            height: width

            anchors {
                top: parent.top
                right: parent.right
            }

            Image {
                source: "qrc:/resources/images/icons/a-delete-button-alt.svg"
                anchors.centerIn: parent

                sourceSize {
                    width: 28
                    height: width
                }
            }

            Custom.HandMouseArea {
                onClicked: {
                    notificationWindow.destroyNotification()
                }
            }
        }
    }
}
