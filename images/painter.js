getUIStyle = () => {
    // Добавляем стили
    const styles = `
    .button_style {
        width: 130px;
        margin-right: 70px;
        background: #513810;
        box-shadow: 0px 6px 0px #2f2009;
        border-radius: 10px;
        border: 4px #704e18 solid;
        cursor: url(../img/cursor1.png), pointer;
        font-family: "Baloo Paaji";
        color: white;
        outline: none;
        font-size: 20px;
        float: right;
        margin-bottom: 20px;
        margin-left: 200px;
    }
    .button_style:hover {
        background: #5c3f11;
        border: 4px #79551b solid;
    }

    #option_in_game {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #chronoquest {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #shop_market {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #home_craft {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #recipe_craft {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #sure_delete {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #cancel_sure_delete {
        opacity: ${Settings.fastOpenUI.otherO};
    }

    #myNewImage {
        opacity: ${Settings.miniMap.o};
        display: ${Settings.miniMap.e ? '' : 'none'};
    }

    #agree_opt {
        width: 35px;
        height: 35px;
        border-radius: 7px;
        text-align: center;
        cursor: url(../img/cursor1.png), pointer;
        border: solid 2px #755219;
        box-shadow: 0px 5px #302009;
        float: left;
        display: inline-block;
        position: absolute;
        top: 245px;
        left: 160px;
        outline: none;
    }

    #script_menu {
        cursor: url(../img/cursor0.png), auto;
        position: absolute;
        width: 550px;
        background: #3A2A0D;
        border: 6px #513810 solid;
        box-shadow: -5px 6px 0px #302009;
        box-sizing: border-box;
        border-radius: 14px;
        font-size: 20px;
        font-weight: normal;
        text-shadow: 0px 2px 0px #281806;
        text-align: center;
        padding-top: 40px;
        padding-bottom: 10px;
        color: #FFFFFF;
        opacity: ${Settings.fastOpenUI.o};
        font-family: "Baloo Paaji";
        outline: none;
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        display: inline-block;
    }
    #script_menu:before {
        content: "SCRIPT MENU";
        background: #443110;
        border: 5px #513810 solid;
        box-shadow: 0px 6px 0px #221605;
        border-radius: 14px;
        color: #745018;
        width: 150px;
        height: 35px;
        display: block;
        position: absolute;
        top: -25px;
        left: 82.5%;
        margin-left: -47%;
    .keyboard-option {
        padding: 5px 10px;
        margin: 5px;
        color: white;
        cursor: pointer;
    }
    #azerty_ing {
        background-color: rgb(58, 42, 13);
    }
    #qwerty_ing {
        background-color: rgb(181, 109, 24);
    }
    #high_ing {
        background-color: rgb(181, 109, 24);
    }
    #low_ing {
        background-color: rgb(58, 42, 13);
    }

    `;
    return styles;
}


colors = () => {
    if (!unsafeWindow.ReiditeSpikeAlly) {
        loadSpikes();
    };
    return
}

loadSpikes = () => {
    let chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ_0123456789";

    for (let e in unsafeWindow) {
        if (!Array.isArray(unsafeWindow[e]) && chars.includes(e[0])) continue;
        if (unsafeWindow[e].length > 800 && unsafeWindow[e].length < 1500) {
            unsafeWindow.sprite = unsafeWindow[e];
        }
    }
}

send = (data) => {
    try {
        client[Object.keys(client)[0]].send(JSON.stringify(data));
    } catch (error) {
        if (script.user.alive) {
            Settings.textalert.t = 'Error loading script'
            Settings.textalert.e = true
            return
        }
    }
}

loadSpectator = () => {
    requestAnimationFrame(loadSpectator);
    if (client[Object.keys(client)[0]]) {
        if (!client[Object.keys(client)[0]]["current"]) {
            client[Object.keys(client)[0]]["current"] = true;
            client[Object.keys(client)[0]].send = new Proxy(client[Object.keys(client)[0]].send, {
                apply: function (target, thisArg, args) {
                    if (args[0][0] == 11 && Settings.spectator.e && !Settings.PathFinder.e && !Settings.Autofarm.e) {
                        return
                    }
                    if (typeof args[0] == 'string') {
                        const obj = JSON.parse(args[0]);
                        if (obj[0] == 28) {
                            mp = script.world.fast_units[script.user.uid];
                            if (mp) {
                                Settings.antiKick.dx = Math.round(obj[1] - mp.x)
                                Settings.antiKick.dy = Math.round(obj[2] - mp.y)
                            }
                        }
                    }
                    return target.apply(thisArg, args);
                }
            });
            const oldFunction = client[Object.keys(client)[68 + 1]];
            client[Object.keys(client)[68 + 1]] = function () {
                if (Settings.spectator.e) return
                oldFunction.apply(this, arguments);
            }
            const userCam = user[Object.keys(user)[28]];
            const moveCam = userCam[Object.keys(userCam)[12]];
            userCam[Object.keys(userCam)[12]] = function () {
                moveCam.apply(this, arguments);
                if (Settings.spectator.e || Settings.spectator.is_back) {
                    userCam.x = Settings.spectator.x;
                    userCam.y = Settings.spectator.y;
                }
            }
        }
    }
    if (!script.user.alive) return

    if (Settings.spectator.e && !Settings.spectator.is_back) {
        if (Settings.spectator.is_x > 0) Settings.spectator.x += Settings.spectator.s;
        if (Settings.spectator.is_x < 0) Settings.spectator.x -= Settings.spectator.s;
        if (Settings.spectator.is_y > 0) Settings.spectator.y += Settings.spectator.s;
        if (Settings.spectator.is_y < 0) Settings.spectator.y -= Settings.spectator.s;
    }
    if (Settings.spectator.is_back) {

        dist = Math.sqrt((Settings.spectator.x - Settings.spectator.start_x) ** 2 + (Settings.spectator.y - Settings.spectator.start_y) ** 2)
        if (dist < 10) {
            Settings.spectator.is_back = false;
        } else {
            dt = Date.now() - Settings.spectator.timeout;
            dx = Settings.spectator.start_x - Settings.spectator.end_x
            dy = Settings.spectator.start_y - Settings.spectator.end_y
            Settings.spectator.x = Settings.spectator.end_x + (dx * Settings.spectator.s * dt / 4000)
            Settings.spectator.y = Settings.spectator.end_y + (dy * Settings.spectator.s * dt / 4000)
            if (Settings.spectator.end_x > Settings.spectator.start_x) {
                if (Settings.spectator.x < Settings.spectator.start_x) Settings.spectator.x = Settings.spectator.start_x;
            } else {
                if (Settings.spectator.x > Settings.spectator.start_x) Settings.spectator.x = Settings.spectator.start_x;
            }
            if (Settings.spectator.end_y > Settings.spectator.start_y) {
                if (Settings.spectator.y < Settings.spectator.start_y) Settings.spectator.y = Settings.spectator.start_y;
            } else {
                if (Settings.spectator.y > Settings.spectator.start_y) Settings.spectator.y = Settings.spectator.start_y;
            }
        }

    }

}