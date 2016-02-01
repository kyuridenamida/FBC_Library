#include <string>
#include <fstream>
#include <iterator>
#include <cassert>
#include <sstream>
#include <fstream>
#include <vector>
#include <iostream>
using namespace std;
class FBCIterator;
class FBC;
 
class FBC
{
friend FBCIterator;
public:
	typedef FBCIterator iterator;
	FBC::iterator begin();
	FBC::iterator end();
private:
	int T;
	size_t caseNum;
public:
	string filename;
	ifstream ifs;
	vector<int> caseStartPos,caseEndPos;
	
	string itos(long long n){
		stringstream ss;
		ss << n;
		return ss.str();
	}
	void init(string filename_){
		filename = filename_;
		ifs.open(filename);
		assert( ifs.is_open() );
	}
	
	int readT(){
		ifs >> T;
	}
	int putCase(){
		if( T == 1 ) ifs >> caseNum;
		cout << "Case #" << caseNum << ": ";
	}
	bool nextIsEnd = false;
	void caseStart(){
		assert( !nextIsEnd );
		caseStartPos.push_back(ifs.tellg());
		nextIsEnd ^= 1;
	}
	void caseEnd(){
		assert( nextIsEnd );
		caseEndPos.push_back(ifs.tellg());
		nextIsEnd ^= 1;
	}
	void dump(string dirname){
		assert( !nextIsEnd );
		for(int i = 0 ; i < caseStartPos.size() ; i++){
			ifstream ifs2(filename);
			char tmp[256];
			sprintf(tmp,"%s/%03d.txt",dirname.c_str(),i+1);
			ofstream ofs(tmp);
			cerr << (dirname+"/" + itos(i+1) + ".txt") << endl;
			assert( ofs.is_open());
			ofs << "1";
			ifs2.seekg(caseStartPos[i],ifs2.beg);
			cerr << caseStartPos[i] << " " << caseEndPos[i] << " " << ifs2.tellg() << endl;
			while( ifs2.peek() != EOF && caseEndPos[i] != ifs2.tellg() ){
				ofs << (char)ifs2.get();
			}
			ofs << endl;
			ofs << i+1 << endl;
			ofs.close();
		}
	}
};

class FBCIterator : public std::iterator<std::forward_iterator_tag, int>
{
friend FBC;

private:
	FBC* fbc;
private:
	FBCIterator() : fbc(nullptr){}
	FBCIterator(FBC* fbc) : fbc(fbc){}
public:
	FBCIterator& operator++(){
		this->fbc->caseEnd();
		if( ++(this->fbc->caseNum) > this->fbc->T )
			this->fbc->caseNum = SIZE_MAX;
		return *this;
	}
	size_t operator*(){
		return fbc->caseNum;
	}
	bool operator!=(const FBCIterator& iterator){
		auto size = [](FBC *ptr){ return ptr == nullptr ? SIZE_MAX : ptr->caseNum; };
		
		if(  size(this->fbc) != size(iterator.fbc) ){
			// まだendじゃない
			this->fbc->caseStart();
			return true;
		}else{
			return false;
		}
	}
};
FBC::iterator FBC::begin()
{
	this->caseNum = 1;
	readT();
	return FBCIterator(this);
}
FBC::iterator FBC::end()
{	
	return FBCIterator();
}

