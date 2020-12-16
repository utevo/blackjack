import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import Model 1.0 // https://stackoverflow.com/questions/57742024/custom-object-referencing-in-qml-python

Window {
    id: window
    width: 640
    height: 480
    visible: true
    title: qsTr("BlackJack")
    color: "green"

        Model {
            id: mainModel
        }


    component Card: Rectangle {
        property int size: 20
        width: 2.5 * size
        height: 3.5 * size
        color: "white"
        radius: 10
    }

    Row {
        id: row
        anchors.bottom: parent.bottom
        anchors.rightMargin: 220
        anchors.leftMargin: 220
        anchors.bottomMargin: 0
        anchors.left: parent.left
        anchors.right: parent.right
        spacing: 20

       RoundButton {
            id: hitButton
            text: 'Hit'
            font.pointSize: 20
            width: parent.parent.width * 0.2
            height: width
            onClicked: mainModel.hit()
       }

       RoundButton {
            id: standButton
            text: 'Stand'
            font.pointSize: 20
            width: parent.parent.width * 0.2
            height: width
            onClicked: mainModel.stand()
       }

       RoundButton {
            id: testButton
            text: 'Test'
            font.pointSize: 20
            width: parent.parent.width * 0.2
            height: width
            onClicked: console.log(mainModel.player_cards)
       }
    }


}


