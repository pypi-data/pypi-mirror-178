import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
/*
    A component that, when created, writes the given values to the initialValues from the listeningValues
    and checks whether they match or not. There is signal changeInitialValues, by calling
    which we can overwrite the data in the initialValues in order to apply the changes.
*/

//  List of values that may change
    property var listeningValues: []
//  List of values that we write after entering the page
    property var initialValues: []
//  Check if there are any changes between listeningValues and  initialValues
    readonly property bool hasChanges: JSON.stringify(listeningValues) != JSON.stringify(initialValues)
//  Signal to rewrite the initialValues
    signal changeInitialValues

    onChangeInitialValues: {
        initialValues = JSON.parse(JSON.stringify(listeningValues))
    }

    Component.onCompleted: {
        changeInitialValues()
    }
}
