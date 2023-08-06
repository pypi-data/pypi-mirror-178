import QtQuick 2.12
import QtQuick.Controls 2.4
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom

AjaxPopup {
    id: popup
    width: 400
    height: 430

    property var sessions: app.security_module.sessions
    property var filteredSessions: app.security_module.filtered_sessions

    signal goToChangePasswordSignal

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

        focus: true

//        AjaxPopupCloseHeader {
//            id: closeItem
//            label: tr.security
//
//            Item {
//                id: manualItem
//
//                width: parent.width - 64
//                height: 24
//                anchors {
//                    right: closeItem.icoClose.left
//                    rightMargin: 16
//                    verticalCenter: parent.verticalCenter
//                }
//
//                Image {
//                    id: manualIcon
//                    sourceSize.width: 24
//                    sourceSize.height: 24
//                    source: "qrc:/resources/images/icons/icon_tutorial.svg"
//                    anchors.right: parent.right
//
//                    MouseArea {
//                        anchors.fill: parent
//                        cursorShape: Qt.PointingHandCursor
//
//                        onClicked: {
//                             var locale = client.get_origin_locale()
//                             var link = "http://instructionservice.ops.ajax.systems/2fa?lang=" + locale
//                             Qt.openUrlExternally(link)
//                        }
//                    }
//                }
//            }
//        }

        Item {
            id: closeItem

            width: parent.width
            height: 64

            anchors.top: parent.top

            Image {
                sourceSize.width: 24
                sourceSize.height: 24

                source: "qrc:/resources/images/icons/back.svg"

                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor

                    onClicked: {
                        popup.close()
                    }
                }
            }

            Custom.PopupHeader {
                width: parent.width - 56
                height: 64
                radius: parent.radius
                title: tr.security

                anchors.right: parent.right

                closeArea.onClicked: {
                    popup.close()
                }
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark4
            anchors.top: closeItem.bottom
        }

        View {
            id: view
            width: parent.width
            anchors {
                top: closeItem.bottom
                bottom: parent.bottom
            }

            Column {
                width: view.width
                spacing: 8

                Item {
                    width: 1
                    height: 12
                }

                Item {
                    width: parent.width
                    height: 20
                    Text {
                        text: tr.current_session
                        width: parent.width - 64
                        wrapMode: Text.WordWrap
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Rectangle {
                        width: parent.width - 64
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.bottom: parent.bottom
                        height: 1
                        color: "gray"
                        opacity: 0.2
                    }
                }

                Item {
                    width: parent.width
                    height: 64

                    Rectangle {
                        width: parent.width - 64
                        height: 70
                        color: ui.colors.dark2
                        radius: 8
                        anchors.centerIn: parent

                        Text {
                            text: tr.online
                            color: ui.colors.green1
                            opacity: 0.8
                            font.family: roboto.name
                            font.pixelSize: 14
                            anchors {
                                right: parent.right
                                rightMargin: 12
                                top: parent.top
                                topMargin: 8
                            }
                        }

                        Column {
                            anchors.fill: parent
                            anchors.margins: 8

                            Text {
                                text: {
                                    var label = ""
                                    if (sessions.this_session.application_label) {
                                        label = util.label_correct(sessions.this_session.application_label)
                                    }
                                    if (sessions.this_session.client_version_major) {
                                        label += " "
                                        label += sessions.this_session.client_version_major
                                    }
                                    return label
                                }
                                color: "#fefefe"
                                opacity: 0.8
                                font.family: roboto.name
                                font.pixelSize: 14
                            }

                            Item {
                                width: 1
                                height: 4
                            }

                            Text {
                                text: sessions.this_session.client_device_model + ", " + sessions.this_session.client_os
                                color: "#fefefe"
                                opacity: 0.5
                                font.family: roboto.name
                                font.pixelSize: 13
                                anchors.left: parent.left
                                width: parent.width - 6
                            }

                            Item {
                                width: 1
                                height: 2
                            }

                            Text {
                                text: sessions.this_session.last_connection_ip != "n/a" ? sessions.this_session.last_connection_ip : tr.na
                                color: "#fefefe"
                                opacity: 0.5
                                font.family: roboto.name
                                font.pixelSize: 13
                                anchors.left: parent.left
                                width: parent.width
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                            }
                        }
                    }
                }

                Item {
                    id: warningItem

                    width: parent.width
                    height: 260

                    visible: sessions.legacy_session_exists

                    Rectangle {
                        id: warningRectangle
                        width: parent.width - 64
                        height: columnItem.height + 36
                        radius: 8
                        color: ui.colors.dark2
                        border.width: 1
                        border.color: "#252525"

                        anchors {
                            top: parent.top
                            topMargin: 16
                            horizontalCenter: parent.horizontalCenter

                        }

                        Column {
                            id: columnItem

                            anchors {
                                top: parent.top
                                topMargin: 18
                                left: parent.left
                                leftMargin: 18
                                right: parent.right
                                rightMargin: 18
                            }
                            spacing: 12

                            Item {
                                id: importantItem
                                width: parent.width
                                height: 23
                                anchors.horizontalCenter: parent.horizontalCenter

                                Image {
                                    id: importantLogo
                                    source: "qrc:/resources/images/desktop/icons/ic_info.png"
                                    height: 23
                                    width: 23
                                    anchors.left: parent.left
                                }

                                Text {
                                    width: parent.width
                                    color: "#e3403b"
                                    text: tr.scenario_important_note
                                    font.family: roboto.name
                                    font.pixelSize: 14
                                    anchors {
                                        left: importantLogo.right
                                        leftMargin: 8
                                        verticalCenter: importantLogo.verticalCenter
                                    }
                                }
                            }

                            Text {
                                width: parent.width - 18
                                text: tr.sessions_were_detected
                                wrapMode: Text.Wrap
                                color: ui.colors.light1
                                lineHeight: 1.23
                                font.family: roboto.name
                                font.pixelSize: 14
                            }

                            Item {
                                id: updateItem

                                width: parent.width
                                height: updateText.height
                                anchors.horizontalCenter: parent.horizontalCenter

                                Image {
                                    id: updateLogo
                                    source: "qrc:/resources/images/desktop/icons/ico_reload.svg"
                                    sourceSize.height: 26
                                    sourceSize.width: 26
                                    anchors.left: parent.left
                                }

                                Text {
                                    id: updateText

                                    height: contentHeight
                                    width: parent.width - 32
                                    color: ui.colors.light1
                                    text: tr.update_app_for_sessions
                                    font.family: roboto.name
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    lineHeight: 1.23
                                    anchors {
                                        left: updateLogo.right
                                        leftMargin: 8
                                    }
                                }
                            }

                            Item {
                                id: killSessionManuallyItem

                                width: parent.width
                                height: changeText.height
                                anchors.horizontalCenter: parent.horizontalCenter

                                Image {
                                    id: killSessionManuallyLogo
                                    source: "qrc:/resources/images/desktop/icons/ico_2fa.svg"
                                    sourceSize.height: 20
                                    sourceSize.width: 14
                                    anchors.left: parent.left
                                    anchors.leftMargin: 6
                                }

                                Text {
                                    id: changeText

                                    height: contentHeight
                                    width: parent.width - 38
                                    color: ui.colors.light1
                                    text: util.insert(tr.kill_session_manually, ['<a href="userSettings" style="color: #60e3ab; text-decoration: none;">', "</a>", '<a href="twoFa" style="color: #60e3ab; text-decoration: none">', "</a>"])
                                    font.family: roboto.name
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    textFormat: Text.RichText
                                    lineHeight: 1.23
                                    onLinkActivated: {
                                        if (link == "userSettings") {
                                            application.goToChangePasswordSignal()
                                            popup.close()
//                                            application.toUserSettings()
                                        } else {
                                            popup.close()
                                        }
                                        popup.close()
                                    }

                                    onLinkHovered: {
                                        if (link) {
                                            cursorShape.cursorShape = Qt.PointingHandCursor
                                        } else {
                                            cursorShape.cursorShape = Qt.ArrowCursor
                                        }
                                    }


                                    MouseArea {
                                        id: cursorShape
                                        cursorShape: Qt.PointingHandCursor
                                        enabled: false
                                        hoverEnabled: false
                                        propagateComposedEvents: true
                                        onPressed: mouse.accepted = false
                                        anchors.fill: parent
                                    }

                                    anchors {
                                        left: killSessionManuallyLogo.right
                                        leftMargin: 14
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    width: 1
                    height: {
                        if (!visible) return 0
                        return 4
                    }

                    visible: sessions.length
                }

                Item {
                    width: parent.width
                    height: {
                        if (!visible) return 0
                        return 20
                    }

                    visible: sessions.length

                    Text {
                        id: activeSessionsLabel

                        text: tr.active_sessions
                        width: parent.width - 64
                        wrapMode: Text.WordWrap
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        anchors.horizontalCenter: parent.horizontalCenter
                        opacity: 0.8
                    }

                    Image {
                        id: image
                        anchors {
                            right: activeSessionsLabel.right
                            verticalCenter: activeSessionsLabel.verticalCenter
                            verticalCenterOffset: -3
                        }
                        source: "qrc:/resources/images/desktop/button_icons/refresh.svg"

                        RotationAnimation on rotation {
                            id: refreshAnim
                            loops: 1
                            from: 0
                            to: 360
                            running: false
                            duration: 500
                        }
                    }

                    MouseArea {
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        anchors.fill: parent
                        onClicked: {
                            refreshAnim.stop()
                            refreshAnim.start()
                            app.security_module.get_sessions()
                        }
                    }

                    Rectangle {
                        width: parent.width - 64
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.top: parent.bottom
                        height: 1
                        color: "gray"
                        opacity: 0.2
                    }
                }

                Item {
                    width: parent.width
                    height: {
                        if (!sessions.length) return 0
                        return listView.contentHeight + 12
                    }

                    ListView {
                        id: listView
                        width: parent.width - 64
                        height: contentHeight
                        anchors.horizontalCenter: parent.horizontalCenter

                        model: filteredSessions
                        spacing: 8

                        interactive: false

                        header : Item {
                            width: parent.width
                            height: {
                                if (!visible) return 0
                                return killAllLabel.contentHeight + 12 + 12
                            }

                            visible: sessions.length

                            Rectangle {
                                width: parent.width
                                height: parent.height - 8
                                color: ui.colors.dark2
                                radius: 8

                                anchors.top: parent.top

//                                visible: sessions.length
                                Text {
                                    id: killAllLabel
                                    width: parent.width - 64
                                    text: tr.terminate_other_sessions
                                    color: "#e3403b"
                                    wrapMode: Text.Wrap
                                    horizontalAlignment: Text.AlignLeft
                                    font.pixelSize: 14
                                    opacity: 0.8
                                    anchors {
                                        left: parent.left
                                        leftMargin: 8
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onEntered: {
                                        killAllLabel.opacity = 1.0
                                    }
                                    onExited: {
                                        killAllLabel.opacity = 0.8
                                    }

                                    onClicked: {
                                        Popups.terminate_session_warning_popup(
                                            sessions.length == 1 ? tr.log_out_pay_attention : tr.log_out_pay_attention_devices,
                                            function() { app.security_module.kill_sessions(sessions.sessions(), true) },
                                            false
                                        )
                                    }
                                }
                            }
                        }

                        delegate: Rectangle {
                            width: parent.width
                            height: 70
                            color: ui.colors.dark2
                            radius: 8

                            Text {
                                text: time_str
                                color: "#fefefe"
                                opacity: 0.8
                                font.family: roboto.name
                                font.pixelSize: 14
                                anchors {
                                    right: parent.right
                                    rightMargin: 12
                                    top: parent.top
                                    topMargin: 8
                                }

                                visible: session.session_refresh_timestamp != 0
                            }

                            Text {
                                id: terminateLabel

                                text: tr.terminate_session
                                color: "#e2252b"
                                opacity: 0.8
                                font.family: roboto.name
                                font.pixelSize: 14
                                anchors {
                                    right: parent.right
                                    rightMargin: 12
                                    bottom: parent.bottom
                                    bottomMargin: 8
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onEntered: {
                                        terminateLabel.opacity = 1.0
                                    }
                                    onExited: {
                                        terminateLabel.opacity = 0.8
                                    }

                                    onClicked: {
                                        Popups.terminate_session_warning_popup(tr.log_out_pay_attention, function() {
                                            app.security_module.kill_sessions([session.session_id], true)
                                        }, false)
                                    }
                                }
                            }

                            Column {
                                anchors.fill: parent
                                anchors.margins: 8

                                Text {
                                    text: {
                                        var label = ""
                                        if (session.application_label) {
                                            label = util.label_correct(session.application_label)
                                        }
                                        if (session.client_version_major) {
                                            label += " "
                                            label += session.client_version_major
                                        }
                                        return label
                                    }
                                    color: "#fefefe"
                                    opacity: 0.8
                                    font.family: roboto.name
                                    font.pixelSize: 14
                                }

                                Item {
                                    width: 1
                                    height: 4
                                }

                                Text {
                                    text: session.client_device_model + ", " + session.client_os
                                    color: "#fefefe"
                                    opacity: 0.5
                                    font.family: roboto.name
                                    font.pixelSize: 13
                                    anchors.left: parent.left
                                }

                                Item {
                                    width: 1
                                    height: 2
                                }

                                Text {
                                    text: session.last_connection_ip != "n/a" ? session.last_connection_ip : tr.na
                                    width: parent.width - 96
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    color: "#fefefe"
                                    opacity: 0.5
                                    font.family: roboto.name
                                    font.pixelSize: 13
                                    anchors.left: parent.left
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: app.login_module

        onLoginFailed: {
            popup.close()
        }

        onLogoutSignal: {
            popup.close()
        }
    }
}
