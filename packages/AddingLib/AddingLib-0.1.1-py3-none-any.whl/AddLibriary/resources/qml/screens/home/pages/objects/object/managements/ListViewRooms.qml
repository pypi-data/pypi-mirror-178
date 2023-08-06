import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.ListView {
    id: rooms

    property var withoutSettingIcon: false
    property var reindexNeeded: true

    Connections {
        target: rooms.list.model

        onLengthChanged: {
            rooms.list.currentIndexChanged()
        }
    }

    Connections {
        target: management

        onResetCurrentIndexes: {
            if (!rooms.reindexNeeded) return

            rooms.reindexNeeded = false
            rooms.list.currentIndex = rooms.list.model.length > 0 ? 0 : -1
        }
    }

    contentPadding: 0
    list {
        spacing: 1
        delegate: RoomDelegate {
            settingsVisible: !withoutSettingIcon
        }
    }
}