import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


Loader {
    id: blockLoader
    z: 1000
    active: false
    asynchronous: true
    anchors.fill: parent

    property var radius: 24
    property var minTime: 0
    property var startSignals: []
    property var stopSignals: []

    property var loadingNow: false
    property var customOpacity: 0.2
    property var backgroundRadius: 0
    property var backgroundColor: ui.colors.black

    signal startSignal()
    signal stopSignal()

    function startit() {
        if (!blockLoader) return
        blockLoader.loadingNow = true
        if (blockLoader.minTime) timer.start()
        active = true
    }

    function stopit() {
        if (!timer) return
        blockLoader.loadingNow = false
        if (timer.running) return
        active = false
    }

    Timer {
        id: timer
        interval: blockLoader.minTime
        repeat: false
        running: false

        onTriggered: {
            if (blockLoader.loadingNow) return
            active = false
        }
    }

    sourceComponent: Item {
        anchors.fill: parent

        Rectangle {
            color: blockLoader.backgroundColor
            opacity: blockLoader.customOpacity
            radius: blockLoader.backgroundRadius
            anchors.fill: parent
        }

        Anime.SharinganLoader {
            id: anim
            radius: blockLoader.radius
            color: ui.colors.green1
            useCircle: true
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -4
        }

        Custom.HandMouseArea {
            cursorShape: Qt.ArrowCursor
        }
    }

    Component.onCompleted: {
        for (var i = 0; i < blockLoader.startSignals.length; i++) {
            blockLoader.startSignals[i].connect(blockLoader.startit)
        }

        for (var i = 0; i < blockLoader.stopSignals.length; i++) {
            blockLoader.stopSignals[i].connect(blockLoader.stopit)
        }
    }
}
