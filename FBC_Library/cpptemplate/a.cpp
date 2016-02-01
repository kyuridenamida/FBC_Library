/*
	[Solution]
	Facebook Hacker Cup 2016 Round 2
	Boomerang Decoration
	https://www.facebook.com/hackercup/problem/424794494381569/
*/
#include <bits/stdc++.h>
#include <alloca.h>
#include "./fbclib.hpp"
using namespace std;

FBC fbc;
#define cin fbc.ifs

string A,B;
int dp[100010][26][2];
int dp2[100010][26][2];

int dfs1(int x,int col,int unchg){
	if( x == -1 ) return 0;
	if( dp[x][col][unchg] != -1 ) return dp[x][col][unchg];
	int ans;
	if( (unchg?A[x]:col + 'A') != B[x] ){
		ans = dfs1(x-1,B[x]-'A',0) + 1;
	}else{
		ans = dfs1(x-1,col,unchg);
	}
	return dp[x][col][unchg] = ans;
}
int dfs2(int x,int col,int unchg){
	if( x == B.size() ) return 0;
	if( dp2[x][col][unchg] != -1 ) return dp2[x][col][unchg];
	int ans;
	if( (unchg?A[x]:col + 'A') != B[x] ){
		ans = dfs2(x+1,B[x]-'A',0) + 1;
	}else{
		ans = dfs2(x+1,col,unchg);
	}
	return dp2[x][col][unchg] = ans;
}

#define cin fbc.ifs
void solve(){
	memset(dp,-1,sizeof(dp));
	memset(dp2,-1,sizeof(dp2));
	int N;
	cin >> N;
	cin >> A >> B;
	for(int i = 0 ; i < 26 ; i++){
		for(int j = 0 ; j < N ; j++){
			dfs1(j,i,0);
			dfs2(N-j,i,0);
			dfs1(j,i,1);
			dfs2(N-j,i,1);	
		}
	}
	int ans = 1e9;
	for(int i = 0 ; i <= N ; i++){
		ans = min(ans,max(dfs1(i-1,0,1),dfs2(i,0,1)));
	}
	fbc.putCase();
	cout << ans << endl;
}
#undef cin


int main(int argc,char *argv[]){
	if( argc < 2 ) {
		cerr << "[Error] no input" << endl;
		exit(1);
	}else{
		fbc.init(argv[1]);
	}
	for( auto ____ : fbc ){
		solve();
	}
}