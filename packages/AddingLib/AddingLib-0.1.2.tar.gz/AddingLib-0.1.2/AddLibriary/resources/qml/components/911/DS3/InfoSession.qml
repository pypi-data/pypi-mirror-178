import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: infoSession

//  Set the version of ajax app
    property string sessionVersion: ""
//  Set device
    property string sessionDevice: ""
//  Set ip
    property string sessionIp: ""
//  Set date
    property string sessionDate: ""
//  Set time
    property string sessionTime: ""
//  Use this to change type of item (Online/Terminate)
    property bool isCurrentSession: false

    signal clicked()

    width: parent.width || 375
    height: !!sessionIp || !!sessionDate ? 88 : 68

    color: ui.ds3.bg.highest

    DS3.AtomTitle {
        id: mainTitle

        width: parent.width - dateTitle.width
        height: 44

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 16
        }

        title: sessionVersion
        subtitle: sessionDevice
    }

    DS3.AtomTitle {
        id: ipTitle

        width: parent.width - dateTitle.width
        height: !!sessionIp ? 20 : 0

        anchors {
            top: mainTitle.bottom
            left: parent.left
            leftMargin: 16
        }

        subtitle: sessionIp
    }

    DS3.Text {
        id: dateTitle

        height: 20

        anchors {
            top: parent.top
            topMargin: 12
            right: parent.right
            rightMargin: 16
        }

        color: ui.ds3.figure.nonessential
        visible: !isCurrentSession
        text: sessionDate
    }

    DS3.Text {
        id: timeTitle

        height: 20

        anchors {
            top: dateTitle.bottom
            right: parent.right
            rightMargin: 16
        }

        color: ui.ds3.figure.nonessential
        visible: !isCurrentSession
        text: sessionTime
    }

    DS3.ButtonTextRect {
        id: buttonText

        anchors {
            bottom: parent.bottom
            right: parent.right
        }

        visible: !isCurrentSession
        status: DS3.ButtonRect.Status.Attention
        isIconLeft: false
        text: tr.terminate_session
        buttonText.style: ui.ds3.text.body.MRegular

        onClicked: infoSession.clicked()
    }

    DS3.Text {
        id: onlineStatus

        anchors {
            top: parent.top
            topMargin: 12
            right: parent.right
            rightMargin: 16
        }

        text: tr.online
        color: ui.ds3.figure.interactive
        visible: isCurrentSession
    }
}