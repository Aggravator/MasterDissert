#include <iostream>

using namespace std;

struct parameters
{
  	double eta; // ����������� ������������� �����
  	double v0; // ������������ ��������� �������� �������� ������
  	double tau; // ��� �������
  	double alpha; // ����� 
  	double beta; // ����
  	bool printpopulation; // ������ ���� ���������
  	bool printbestsolution; // ������ ������� �������
  	bool printstatistics; // ������ �������� � ������� �������� ������� �������
  	parameters()
  	{
    		eta = 0.9; 
    		v0 = 1.0; 
    		tau = 1.0; 
    		alpha = 0.5; 
    		beta = 0.5; 
    		printpopulation = 0; 
    		printbestsolution = 1; 
    		printstatistics = 1; 
  	}
};

// ����� �������� ������� �������
bool better(double a, double b)
{
	return a<b;
}
// ����������� ������� ��������� ��������������������
double target(int* x, int n)
{
	double sum = 0;
	for( int i=0; i<n; i++ )
		sum += x[i];
	return sum;
}
struct population
{
	int n; // ����������� ������
	int m; // ������ ���������
	int* data; 
	double* fitness;
	double* p; // ������ ����� ��������� �������
	double* v; // ������ �������� �������
	population(int n_, int m_)
	{
		init(n_,m_);
	}
	population(const population &P){
		init(P.n,P.m);
		copy(P);
	}
	void init(int n_, int m_)
	{
 		n = n_;
		m = m_;
		data = new int[n*m];
		fitness = new double[m];
    		p = new double[n*m];
    		v = new double[n*m];
	}
	void copy(const population &P){
		std::copy(P.data,P.data+n*m,data);
		std::copy(P.fitness,P.fitness+m,fitness);
			std::copy(P.p,P.p+m,p);
			std::copy(P.v,P.v+m,v);
	}
	
	population& operator=(const population& P){
		if(this!=&P){
			if(P.m!=m || P.n!=n){
				this->~population();
				init(P.n,P.m);
			}
			copy(P);
		}
		return *this;
	}
  	~population()
  	{
   		delete[] data;
		delete[] fitness;
    		delete[] p;
    		delete[] v;
  	}
};

void update_global(population& P, double* g)
{
	int n = P.n; // ����������� ������
	int m = P.m; // ������ ��������� 
	int best = 0;
	for( int i=0; i<m; i++ )
		if( better(P.fitness[i], P.fitness[best]) )
			best = i;
	for( int k=0; k<n; k++ )
		g[k] = P.data[best*n+k];
}

double randreal(double a, double b)
{
	return a+(b-a)*(double(rand())/RAND_MAX);
}

void randrealfill(double* x, int n, double min_value, double max_value)
{
 	for( int i=0; i<n; i++ )
		x[i] = randreal(min_value,max_value);
}
void init(population& P, parameters& par)
{
	int n = P.n; // ����������� ������
	int m = P.m; // ������ ��������� 
	for( int i=0; i<m; i++ )
	{
		randrealfill(P.data+i*n, n, par.min_value, par.max_value);
		P.fitness[i] = target(P.data+i*n, n);
		randrealfill(P.v+i*n, n, -par.v0, par.v0);
		for( int k=0; k<n; k++ )
			P.p[i*n+k] = P.data[i*n+k];
	}
}

void update_particle(population& P, int i, double* g, parameters& par)
{
	int n = P.n;
	double alpha = par.alpha;
	double beta = par.beta;	for( int k=0; k<n; k++ )
	{
		P.v[i*n+k] = par.eta*P.v[i*n+k] + alpha*(P.p[i*n+k]-P.data[i*n+k]) + beta*(g[k]-P.data[i*n+k]);
		P.data[i*n+k] += par.tau*P.v[i*n+k];
	}
	double f = target(P.data+i*n, n);
	if( better(f, P.fitness[i]) )
		for( int k=0; k<n; k++ )
			P.p[i*n+k] = P.data[i*n+k];	
	P.fitness[i] = f;		
}

// ������ ������ � ������� ���������: ��� �������, ������ �������, ����������
void print_population(population& P, parameters& par)
{
	int n = P.n;
	int m = P.m;
	if( par.printpopulation )
		for( int i=0; i<m; i++ )
		{
			cout << P.fitness[i] << " ";
			for( int j=0; j<n; j++ )
				cout << P.data[i*n+j] << " ";
			cout << endl;
		}	
	double average_target = 0.0;
	int best = 0;
	for( int i=1; i<m; i++ )
	{
		if( better(P.fitness[i], P.fitness[best]) )
			best = i;
		average_target += P.fitness[i];
	}
	average_target /= m;
	if( par.printbestsolution )
	{
		for( int k=0; k<n; k++ )
			cout << " " << P.data[best*n+k];
		cout << endl;
	}
	if( par.printstatistics )
		cout << P.fitness[best] << " " << average_target << endl;
}
// // ����������� ������ ������ ��� ������
void run_psoa(parameters& par)
{
	population P(par.task_dim, par.pop_size);
	double* g = new double[par.task_dim];
	init(P, par);
	update_global(P, g);
	for( int t=0; t<par.generations; t++ )
	{
		for( int i=0; i<par.pop_size; i++ )
			update_particle(P, i, g, par);
		update_global(P, g);
		print_population(P, par);
	}	
	delete[] g;
}

int main(int argc, char** argv)
{
	parameters par;
	run_psoa(par);
	return 0;
}        
