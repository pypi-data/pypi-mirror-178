import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/" as Root
import "qrc:/resources/qml/components/911/DS3" as DS3


Root.ContextLoader {
    id: accessCodesContextLoader

    contextTarget: app.accessCodes
}

