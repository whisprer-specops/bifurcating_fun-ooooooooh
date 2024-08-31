import requests
import threading
import time
import random
import aiohttp
import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt

# Rotating proxy class with IPv4 and IPv6 proxies
class ProxyPool:
    def __init__(self):
        self.ipv6_proxies = [
            {"proxy": "http://ipv6_proxy1:port", "weight": 5, "failures": 0},
            {"proxy": "http://ipv6_proxy2:port", "weight": 2, "failures": 0},
            {"proxy": "http://ipv6_proxy3:port", "weight": 1, "failures": 0},
        ]
        self.ipv4_proxies = [
            {"proxy": "http://ipv4_proxy1:port", "weight": 5, "failures": 0},
            {"proxy": "http://ipv4_proxy2:port", "weight": 3, "failures": 0},
            {"proxy": "http://ipv4_proxy3:port", "weight": 1, "failures": 0},
        ]
        self.max_failures = 3

    def get_proxy(self, ipv6=True):
        proxies = self.ipv6_proxies if ipv6 else self.ipv4_proxies
        total_weight = sum(proxy["weight"] for proxy in proxies)
        random_choice = random.uniform(0, total_weight)
        cumulative_weight = 0
        for proxy in proxies:
            cumulative_weight += proxy["weight"]
            if random_choice <= cumulative_weight:
                return proxy["proxy"]
        return None

    def report_failure(self, proxy_url):
        for proxies in [self.ipv6_proxies, self.ipv4_proxies]:
            for proxy in proxies:
                if proxy["proxy"] == proxy_url:
                    proxy["failures"] += 1
                    if proxy["failures"] >= self.max_failures:
                        print(f"Removing {proxy_url} due to repeated failures")
                        proxies.remove(proxy)
                    break

    def report_success(self, proxy_url):
        for proxies in [self.ipv6_proxies, self.ipv4_proxies]:
            for proxy in proxies:
                if proxy["proxy"] == proxy_url:
                    proxy["failures"] = 0
                    break

# Generate and play bifurcation sound
def generate_bifurcation_sound():
    interval = (2.8, 4)
    accuracy = 0.0001
    reps = 600
    numtoplot = 200
    lims = np.zeros(reps)
    audio_data = []

    lims[0] = np.random.rand()
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])
        for x in lims[reps - numtoplot:]:
            freq = 220 + x * 880  # Map x to sound frequencies
            audio_data.append(freq)

    sampling_rate = 44100
    duration = len(audio_data) / sampling_rate
    t = np.linspace(0, duration, len(audio_data))
    audio_wave = 0.5 * np.sin(2 * np.pi * audio_data * t)
    audio_wave = np.int16(audio_wave / np.max(np.abs(audio_wave)) * 32767)
    write("bifurcation_sound.wav", sampling_rate, audio_wave)

# Asynchronous fetch with proxy support
async def fetch(session, url, proxy_pool, ipv6=True):
    proxy = proxy_pool.get_proxy(ipv6=ipv6)
    headers = {"User-Agent": random.choice(user_agents)}
    try:
        async with session.get(url, proxy=proxy, headers=headers) as response:
            print(f"Request sent via {proxy}, status code: {response.status}")
            proxy_pool.report_success(proxy)
    except Exception as e:
        print(f"Request failed: {e}. Retrying with a different proxy...")
        proxy_pool.report_failure(proxy)

# Main async function to run the requests
async def main():
    proxy_pool = ProxyPool()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(NUM_THREADS):
            tasks.append(fetch(session, URL, proxy_pool))
        await asyncio.gather(*tasks)
    generate_bifurcation_sound()

# User-Agent randomization setup
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
]

# Configuration
URL = "http://example.com"  # Replace with the target URL
NUM_THREADS = 10  # Number of concurrent threads

# Start the bot
if __name__ == "__main__":
    asyncio.run(main())
