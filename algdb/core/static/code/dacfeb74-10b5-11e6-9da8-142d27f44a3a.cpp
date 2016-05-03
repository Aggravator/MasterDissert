#include <algorithm>
#include <iostream>

using namespace std;

struct parameters
{
  	double rank_a; // a
  	double p_cross; // вероятность выполнения скрещивания в заданной паре
  	double p_mut; // вероятность мутации заданного решения
  	double p_mutation_rate; // Вероятность мутации одного гена
  	bool printpopulation; // печать всей популяции
  	bool printbestsolution; // печать лучшего решения
  	bool printstatistics; // печать среднего и лучшего значений целевой функции
  	parameters()
  	{
    		rank_a = 1.5; 
    		p_cross = 0.5; 
    		p_mut = 0.1; 
    		p_mutation_rate = 0.01; 
    		printpopulation = 0; 
    		printbestsolution = 0; 
    		printstatistics = 1; 
  	}
};

// Поиск минимума целевой функции
bool better(double a, double b)
{
	return a<b;
}
// Кодирование решений двоичными последовательностями
double target(int* x, int n)
{
	double sum = 0;
	for( int i=0; i<n; i++ )
		sum += x[i];
	return sum;
}
struct population
{
	int n; // размерность задачи
	int m; // размер популяции
	int* data; 
	double* fitness;
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
	}
	void copy(const population &P){
		std::copy(P.data,P.data+n*m,data);
		std::copy(P.fitness,P.fitness+m,fitness);
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
  	}
};

int randbool()
{
	return rand()%2;
}

void randboolfill(int* x, int n)
{
 	for( int i=0; i<n; i++ )
		x[i] = randbool();
}
void init(population& P, parameters& par)
{
	int n = par.task_dim;
	int m = par.pop_size;
	for( int i=0; i<m; i++ )
	{
		randboolfill(P.data+i*n, n);
		P.fitness[i] = target(P.data+i*n, n);
	}
}

void copy(population& P, int i, int j,population* to=0)
{
	if(to==0)to=&P;
	int n = P.n;
	for( int k=0; k<n; k++ )
	{
		to->data[i*n+k] = P.data[j*n+k];
	}
	to->fitness[i] = P.fitness[j];
}

double randreal(double a, double b)
{
	return a+(b-a)*(double(rand())/RAND_MAX);
}

struct SortIdividsFunctor{
	population& p;
	SortIdividsFunctor(population &p_):p(p_){}
	bool operator()(int i,int j){
		return better(p.fitness[i],p.fitness[j]);
	}
};

// Отбор методом ранжирования
void select_population(population& P, parameters& par)
{                                          
	int n = P.n;
	int m = P.m;
	double a=par.rank_a;
	double b=2-a;
	
	int *sortedIndivids=new int[m];//Отсортированный от лучшего к худшему массив значений целевой функции особей
	double *normFitness=new double[m];//Нормированный массив значений целевой функции особей
	
	for(int i=0;i<m;++i)sortedIndivids[i]=i;
	
	std::sort(sortedIndivids,sortedIndivids+m,SortIdividsFunctor(P));
	
	for(int i=0;i<m;++i)
		normFitness[sortedIndivids[i]]=1/double(m)*(a-(a-b)*double(i)/(m-1));
	
	delete[] sortedIndivids;
	
	population parentPool(n,m);
	double p,pSum;
	int j;
	for(int i=0;i<m;++i){
		p=randreal(0,1);
		pSum=0;
		j=0;
		while(pSum<=p && j<m)
			pSum+=normFitness[j++];
		copy(P,i,j-1,&parentPool);
	}
	
	delete[] normFitness;
	
	P=parentPool;
}
int randint(int a, int b)
{
	return a + rand()%(b-a);
}

// Двухточечное скрещивание
void crossover(population& P, int x, int y, parameters& par)
{
	int n = P.n;
	int j1 = randint(1, n-1);
	int j2 = randint(j1+1, n);
	for( int k=j1; k<j2; k++ )
		swap(P.data[x*n+k], P.data[y*n+k]);
	P.fitness[x] = target(P.data+x*n,n);
	P.fitness[y] = target(P.data+y*n,n);
}

void shuffle(population& P)
{
	int n = P.n;
	int m = P.m;
	for( int i=0; i<m; i++ )
	{
		int j = randint(i, m);
		for( int k=0; k<n; k++ )
		{
			swap(P.data[i*n+k], P.data[j*n+k]);
		}
		swap(P.fitness[i], P.fitness[j]);
	}
}	


// Схема скрещивания на основе перемешивания популяции
void crossover_population(population& P, parameters& par)
{
	int m = par.pop_size;
	shuffle(P);
	for( int i=0; i<m/2; i++ )
	{
		if( randreal(0,1) < par.p_cross )
			crossover(P, 2*i, 2*i+1, par);
	}
}

// Случайная инверсия каждого бита заданной последовательности 
// с вероятностью p_mutate_rate.
void mutate(population& P, int i, parameters& par)
{
	int n = P.n;
	for( int k=0; k<n; k++ )
		if( randreal(0,1) < p.p_mutation_rate )
			P.data[i*n+k] = !P.dat[i*n+k];
 	P.fitness[i] = target(P.data+i*n, n);
}

// Стандартная схема мутации
void mutate_population(population& P, parameters& par)
{
	int n = P.n;
	int m = P.m;
	for( int i=0; i<m; i++ )
		if( randreal(0,1) < par.p_mut )
			mutate(P, i, par);
}
// Печать данных о текущей популяции: все решения, лучшее решение, статистика
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
// // Стандартная версия генетического алгоритма
void run_ga(parameters& par)
{
	population P(par.task_dim, par.pop_size);
	init(P, par);
	for( int t=0; t<par.generations; t++ )
	{
		select_population(P, par);
		crossover_population(P, par);
		mutate_population(P, par);
		print_population(P, par);
	}	
}

int main(int argc, char** argv)
{
	parameters par;
	run_ga(par);
	return 0;
}        
