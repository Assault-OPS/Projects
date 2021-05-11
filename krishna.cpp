#include <iostream>
#include <vector>
using namespace std;



int max(vector<int> test)
{
    int max_val = 0;
    for(int i=0;i<test.size();i++)
    {
        if(max_val < test[i])
            max_val = test[i];
    }
    return max_val;
} 


int main()
{
    vector<int> data;
    vector<int> backup;
    int limit;
    int values;
    int val;
    //Input Data -------------------------
    cout << "Enter limit: ";
    cin >> limit;
    for(int i=1;i<=limit;i++)
    {
        string x;
        switch(i)
        {
            case 1: x = "st"; break;
            case 2: x = "nd"; break;
            case 3: x = "rd"; break;
            default: x = "th"; break;
        }
        cout << "Enter " << i << x << " value: ";
        cin >> values;
        data.push_back(values);
    }
    backup = data;
    //Data Converter------------------------
    int bruh = max(data);
    for(int i=0;i<data.size();i++)
    {
        val = (data[i]*10)/bruh; // <-- formula to convert data to graph form
        data[i] = val;
    }
    // Bar Graph Maker (MAIN) --------------
    int dynamic_bruh = to_string(bruh).length();
    for(int i=1;i<11;i++)
    {
        cout << "|";  
        if(dynamic_bruh == 1)
            dynamic_bruh += 1;
        for(int j=0;j<data.size();j++)
        {
            if(i>10-data[j])
            {
                for(int i=0;i<dynamic_bruh;i++)
                    cout << "%";
            }
            else
            {
                for(int i=0;i<dynamic_bruh;i++)
                    cout << " ";
            }
            cout << " ";
        }
        cout << endl;
    }
    //X-Axis--------------------------------
    for(int i=0;i<data.size();i++)
    {
        for(int i=0;i<dynamic_bruh+1;i++)
            cout << "-";
    }
    cout << endl << " ";
    for(int i=0;i<backup.size();i++)
    {
        int num_len = to_string(backup[i]).length();
        cout << backup[i];
        for(int i=0;i<dynamic_bruh-num_len;i++)
            cout << " ";
        cout << " ";
    }

    cout << endl;

    //--------------------------------------
}


