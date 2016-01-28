#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    /* if using macbook retina, set to true */
    bool retina = true;
    
    /* setup a grab window, same size as the app */
    grabber.setup(ofGetWidth(), ofGetHeight(), retina);
    
    ofSetWindowPosition(0, 0);
    button = new ofxDatGuiButton("Take Screenshot");
    
    positionButtons();
    
    button->onButtonEvent(this, &ofApp::onButtonEvent);
}

//--------------------------------------------------------------
void ofApp::update(){
    button->update();
}

//--------------------------------------------------------------
void ofApp::draw(){
    button->draw();
    grabber.draw(0, 0);
}

void ofApp::onButtonEvent(ofxDatGuiButtonEvent e)
{
    if (e.target == button){
        button->setLabel("YOU CLICKED ME ONCE");
        grabber.grabScreen(0, 0);
    }
}


void ofApp::positionButtons()
{
    button->setPosition(ofGetWidth()/2 - button->getWidth()/2, ofGetHeight()/2 - button->getHeight());
}