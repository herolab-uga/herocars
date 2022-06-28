using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
namespace UI {
    public class MainMenuUI : MonoBehaviour {
        public Button RACETRACK1_BUTTON;
        public Button RACETRACK2_BUTTON;
        public Button Exit;
        public Button RC_Car_Interface;
        void Start () {
            RACETRACK1_BUTTON.onClick.AddListener (delegate { SceneManager.LoadScene (sceneName: "Racetrack One"); });
            // RACETRACK2_BUTTON.onClick.AddListener (delegate { SceneManager.LoadScene (sceneName: "Racetrack Two"); });
            RC_Car_Interface.onClick.AddListener (delegate { SceneManager.LoadScene (sceneName: "RCCar"); });
            Exit.onClick.AddListener (delegate { Application.Quit(); });
        }
    }
}