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
    int limit;
    int values;
    int val;
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
    int bruh = max(data);
    for(int i=0;i<data.size();i++)
    {
        val = (data[i]*10.0)/bruh;
        data[i] = val;
    }
    for(int i=1;i<11;i++)
    {
        cout << "| ";
        for(int j=0;j<data.size();j++)
        {
            if(i>10-data[j])
                cout << "%% "; 
            else
                cout << "   ";
        }
        cout << endl;
    }
    cout << "--";
    for(int i=0;i<data.size();i++)
        cout << "---";
    cout << endl;
}


