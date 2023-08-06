import QtQuick 2.12
import QtQuick.Controls 2.13


Loader {
    id: loader

    property var contextTarget: null
    readonly property var path: contextTarget ? contextTarget.qml : ""

    width: parent.width
    height: parent.height

    onPathChanged: if (!path) loader.sourceComponent = null

    onContextTargetChanged: {
        if (contextTarget != null) setSource(contextTarget.qml, {"context": contextTarget})
        else loader.sourceComponent = null
    }

    onLoaded: {
        if (!(loader.item instanceof ContextItem) && loader.item != null) {
            console.error("qrc :: ERROR :: Item of ContextLoader must have a ContextItem type.")
            loader.sourceComponent = null
        }
    }
}
