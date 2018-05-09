#### Returns
$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} +  \cdots = \sum_{k=0}^\infty \gamma^k R_{t+k+1}$

#### Value functions
* _state-value function_:  $v_{\pi}(s) = \mathbb{E}_\pi[G_t | S\_t = s]$
* _action-value function_: $q_{\pi}(s,a) = \mathbb{E}_\pi[G_t | S_t = s, A_t =a]$

We will derive a more useful form for these value function equations below. But first, let's re-prove the well known [Law of Iterated Expectations](https://en.wikipedia.org/wiki/Law_of_total_expectation) using our notation for the expected return $G_{t+1}$.

#### Law of iterated expectations
***Theorem***

$\mathbb{E}_{\pi}[\mathbb{E}\_{\pi}[G\_{t+1} | S\_{t+1} = s\']|S\_t = s] = \mathbb{E}\_{\pi}[G\_{t+1} | S\_t = s]$ 


_Proof_: To keep the notation clean and easy to read we'll drop the subscripts, and denote the random variables $s=S_t$, $g'=G_{t+1}$, $s'=S_{t+1}$.

$$
\begin{align}
\mathbb{E}\_{\pi}[G\_{t+1} | S\_{t+1}] 
&= \mathbb{E}\_{\pi}[g\' | s\'] \\\\
&= \sum\_{g'}g\'p(g\' | s\')
\end{align}
$$

Conditioning on $S_t = s$ and taking the expectation of the above expression we get:

$$
\begin {align}
\mathbb{E}\_{\pi}[\mathbb{E}\_\pi[G\_{t+1} | S\_{t+1}] | S_t ]
&= \mathbb{E\}_{\pi}[\mathbb{E}\_\pi[g\' | s\'] |s ] \\\\
&= \sum_{s'} \sum_{g'}g'\, p(g\' | s\', s) \, p(s\' | s)  \\\\
\end{align}
$$

&= \sum_{s'} \sum_{g'}g'\, p(g\' | s\', s) \, p(s\' | s)  \\\\
&= \sum_{s'} \sum_{g'} \frac{g'\, p(g\' | s\', s) \, p(s\' | s) p(s)}{p(s)}  \\\\
&= \sum_{s'} \sum_{g'} \frac{g'\, p(g\' | s\', s) \, p(s'\, s)}{p(s)}  \\\\

$$
\begin {align}
&= \sum_{s'} \sum_{g'} \frac{g'\, p(g\', s\', s)}{p(s)}  \\\\
&= \sum_{s'} \sum_{g'} g'\, p(g\', s\' | s)  \\\\
&= \sum_{g'} \sum_{s'} g'\, p(g', s\' | s)  \\\\
&= \sum_{g'} g'\, p(g\'| s)  \\\\
&= \mathbb{E}\_\pi[g\' | s]
= \mathbb{E}\_\pi[G\_{t+1} | S\_{t}]
\end {align}
$$


## Bellman's Equations
Using the law of iterated expectation, we can expand the state-value function $v_{\pi}(s)$ as follows:
$$
\begin {align}
v_{\pi}(s) &= \mathbb{E}_\pi[G_t | S_t = s] \\
&= \mathbb{E}_\pi[R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} +  \cdots | S_t = s] \\
&= \mathbb{E}_\pi[R_{t+1} + \gamma \sum_{k=0}^\infty \gamma^k R_{(t+1)+k+1} | S_t = s] \\
&= \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} | S_t = s] \\
&= \mathbb{E}_\pi[R_{t+1} + \gamma \mathbb{E}_{\pi}[G_{t+1} | S_{t+1}] | S_t = s] \\
&= \mathbb{E}_\pi[R_{t+1} + \gamma v_{\pi}(S_{t+1}) | S_t = s] \\
&= \sum_a\Pi(a|s) \sum_r p(r | s,a)r + \gamma \sum_a\Pi(a|s) \sum_{s'} p(s' | s,a) v_{\pi} (s') \\
&= \sum_a\Pi(a|s) \sum_r \sum_{s'} p(s', r | s,a)r + \gamma \sum_a\Pi(a|s) \sum_{s'} \sum_r p(s', r | s,a) v_{\pi} (s') \\
&= \sum_a\Pi(a|s) \sum_{s'} \sum_r p(s', r | s,a)r + \gamma \sum_a\Pi(a|s) \sum_{s'} \sum_r p(s', r | s,a) v_{\pi} (s') \\
&= \sum_a\Pi(a|s) \sum_{s'} \sum_r p(s', r | s,a)[r + \gamma v_{\pi} (s')] \\
\end {align}
$$

We can represent this equation as a backup diagram:

Similarly we can rewrite the action-value function $q_{\pi}(s,a)$ as follows:




## Bellman's Optimality Equations









## Summary
In the next section, we're going to
