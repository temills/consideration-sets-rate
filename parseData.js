// This file holds functions for parsing the data 

    //reformat data before saving
    function reformatData(data) {
        var numTrials = 8;
        var startIndex = 4;
        //list of dictionaries, where each dictionary keeps the data for a single trial
        //Those dictionaries will become  rows in the data table
        var allData = [];
        //for (var i=startIndex; i<startIndex+(numTrials*2); i=i+2) {
        for (var i=startIndex; i<startIndex+numTrials; i=i+1) {
            var trialData = {};
            trialData.trial_order = i+1-startIndex;
            trialData.turk_code = JSON.parse(JSON.stringify(data[0]))["turk_code"];
            trialData.subject_id = JSON.parse(JSON.parse(JSON.stringify(data[2]))["responses"])["subject_id"];
            data[i] = JSON.parse(JSON.stringify(data[i]));
            //data[i+1] = JSON.parse(JSON.stringify(data[i+1]));
            trialData.rt = data[i]["rt"];// + data[i+1]["rt"] ;
            var res1 = JSON.parse(data[i]["responses"]);
            //var res2 = JSON.parse(data[i+1]["responses"]);
            trialData.animal = Object.keys(res1)[0].split(", ")[0];
            for (var j=0; j<Object.keys(res1).length; j++) {
                var key = Object.keys(res1)[j].split(", ")[1];
                if (key.includes(" ")) {
                    var tick = "`";
                    key = tick.concat(key, tick);
                }
                var r = String(Object.values(res1)[j]+1);
                r = r.replace(/'/gi, "");
                r = r.replace(/"/gi, "");
                r = r.replace(/;/gi, "");
                r = r.replace(/\//gi, "");
                r = r.replace(/\\/gi, "");
                trialData[key] = r;
            }
            /*
            for (var j=0; j<Object.keys(res2).length; j++) {
                var key = Object.keys(res2)[j].split(", ")[1];
                var r = String(Object.values(res2)[j]);
                r = r.replace(/'/gi, "");
                r = r.replace(/"/gi, "");
                r = r.replace(/;/gi, "");
                r = r.replace(/\//gi, "");
                r = r.replace(/\\/gi, "");
                trialData[key] = r;
            }
            */
            //var demo1 = JSON.parse(JSON.parse(JSON.stringify(data[startIndex+(numTrials*2)]))["responses"]);
            var demo1 = JSON.parse(JSON.parse(JSON.stringify(data[startIndex+numTrials]))["responses"]);
            trialData.age = Object.values(demo1)[0];
            trialData.language = Object.values(demo1)[1];
            trialData.nationality = Object.values(demo1)[2];
            trialData.country = Object.values(demo1)[3];
            //var demo2 = JSON.parse(JSON.parse(JSON.stringify(data[startIndex+(numTrials*2)+1]))["responses"]);
            var demo2 = JSON.parse(JSON.parse(JSON.stringify(data[startIndex+numTrials*+1]))["responses"]);
            trialData.gender = Object.values(demo2)[0];
            trialData.student = Object.values(demo2)[1];
            trialData.education = Object.values(demo2)[2];
            allData.push(trialData);
        }
        return allData;
    }
    
    export function makeQuery(data) {
        data = JSON.parse(JSON.stringify(data));
        console.log("Parsing data");
        data = reformatData(data);
        console.log("done");
        var table = 'zoo_animals2';
        var keys = "";
        var keyArr = Object.keys(data[0]);
        for(var i=0; i<keyArr.length; i++) {
            keys = keys.concat(keyArr[i] + ", ");
        }
        keys = "(" + keys.substring(0, keys.length-2) + ")";
        var valuesList = [];
        var x = 0;
        for(var i=0; i<data.length; i++) {
            var dict = data[i];
            valuesList[x] = "";
            var valArray = Object.values(dict);
            for(var j=0; j<valArray.length; j++) {
                valuesList[x] = valuesList[x].concat("'" + valArray[j] + "', ");
            }
            x++;
        }
        var valuesStr = "";
        for (var i=0; i<valuesList.length; i++) {
            var values = valuesList[i];
            values = "(" + values.substring(0, values.length-2) + ")";
            valuesStr = valuesStr + values + ", ";
        }
        valuesStr = valuesStr.substring(0, valuesStr.length-2);
        console.log("INSERT INTO " + table + keys + " " + "VALUES " + valuesStr + ";");
        return "INSERT INTO " + table + keys + " " + "VALUES " + valuesStr + ";";
    }