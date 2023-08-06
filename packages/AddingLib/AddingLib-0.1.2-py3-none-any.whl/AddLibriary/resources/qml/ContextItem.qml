import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
    property var context

    property var onCompletedArguments: ({})

    onContextChanged: if (!context) parent.sourceComponent = null

    Component.onCompleted: context.onCompleted(JSON.stringify(onCompletedArguments))
    Component.onDestruction: if (!!context) context.onDestruction()
}
